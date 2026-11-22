import logging
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add project root to path to allow imports when running directly
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.llm_service import LLMService
from src.graph_store import GraphStore

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Graph-Augmented Retrieval Pipeline for Codebases.
    Translates questions into entity searches, traverses the Neo4j knowledge graph,
    and synthesizes answers grounded in code topology.
    """
    def __init__(self, provider: Optional[str] = None):
        self.llm = LLMService(provider=provider)
        self.graph_store = GraphStore()

    def get_answer(self, user_question: str) -> str:
        """
        Orchestrates question analysis -> graph traversal -> synthesis.
        """
        logger.info(f"Processing question: {user_question}")
        
        if not self.graph_store.is_connected():
            return (
                "⚠️ Neo4j database is currently disconnected. "
                "Please start Neo4j (e.g. `docker compose up -d`) to enable graph retrieval."
            )

        # 1. Extract target entities or concepts
        search_terms = self._extract_search_terms(user_question)
        context_data = []

        if search_terms:
            logger.info(f"Searching for entities in graph: {search_terms}")
            context_data = self._retrieve_context(search_terms)

        # 2. Fallback to general topology context if specific entity lookup was dry
        if not context_data:
            logger.info("No specific entities matched. Retrieving general structural context...")
            context_data = self._retrieve_general_context()

        if not context_data:
            return (
                "I analyzed the knowledge graph but found no matching code entities or relationships. "
                "Try asking about specific functions, classes, or files in the ingested repository."
            )

        # 3. Synthesize final answer grounded in graph context
        return self._synthesize_answer(user_question, context_data)

    def _extract_search_terms(self, question: str) -> List[str]:
        """Maps user question into entity names, node labels, or code symbols."""
        prompt = f"""Analyze this question about a software codebase graph.
Extract code symbols, entity names (Function names, Classes, Files, Modules) OR concepts.

Rules:
1. If specific symbols/names are mentioned (e.g. "auth.py", "login", "calculate"), return them.
2. If broad questions about dependencies or packages, include "Library".
3. If files or project layout are mentioned, include "File".
4. Return ONLY a JSON list of strings (e.g. ["File", "login"]).

Question: "{question}"
Output:"""
        result = self.llm.get_json_response(prompt)
        if isinstance(result, list):
            return [str(item) for item in result if item]
        return []

    def _retrieve_context(self, entities: List[str]) -> List[Dict[str, Any]]:
        """Queries Neo4j for 1-hop and 2-hop relationships matching given entities."""
        context_results = []
        for entity in entities:
            if entity in ["Library", "File", "Function", "Class"]:
                query = f"""
                MATCH (n:{entity})
                RETURN n.name AS Source, '{entity}' AS Type, '' AS Relationship, '' AS Target
                LIMIT 40
                """
                params = {}
            else:
                query = """
                MATCH (n)-[r]-(m)
                WHERE toLower(n.name) CONTAINS toLower($name)
                RETURN n.name AS Source, type(r) AS Relationship, m.name AS Target
                LIMIT 25
                """
                params = {"name": entity}
            
            results = self.graph_store.query_graph(query, params)
            context_results.extend(results)
        return context_results

    def _retrieve_general_context(self) -> List[Dict[str, Any]]:
        """Fallback: retrieves top connected hubs (files, core libraries) in the graph."""
        query = """
        MATCH (n)
        WHERE n:File OR n:Library OR n:Class
        WITH n, size((n)--()) as degree
        ORDER BY degree DESC
        LIMIT 15
        MATCH (n)-[r]-(m)
        RETURN n.name AS Source, type(r) AS Relationship, m.name AS Target
        LIMIT 40
        """
        return self.graph_store.query_graph(query)

    def _synthesize_answer(self, question: str, context: List[Dict[str, Any]]) -> str:
        context_lines = []
        for item in context[:50]:
            src = item.get("Source", "")
            rel = item.get("Relationship", "")
            tgt = item.get("Target", "")
            if rel and tgt:
                context_lines.append(f"- ({src}) -[{rel}]-> ({tgt})")
            else:
                context_lines.append(f"- Entity: {src} ({item.get('Type', 'Node')})")
        context_str = "\n".join(context_lines)

        prompt = f"""You are a Principal Software Architect assisting a developer with understanding their codebase.
Answer the developer's question accurately using ONLY the Knowledge Graph relationships below.

**Knowledge Graph Context:**
{context_str}

**User Question:**
{question}

**Architect's Answer:**"""
        return self.llm.get_response(prompt)

    def close(self):
        self.graph_store.close()
