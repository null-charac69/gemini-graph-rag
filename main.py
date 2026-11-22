import os
import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.ingestion import FileIngestor
from src.extractor import GraphExtractor
from src.graph_store import GraphStore
from src.rag_pipeline import RAGPipeline

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("CodeGraphRAG")


def build_knowledge_graph(repo_path: str = "data", provider: str = None, wipe_existing: bool = False):
    """
    Scans a source code repository, chunks code, extracts structure, and saves to Neo4j.
    """
    logger.info(f"🏗️ Starting Code Graph Construction for repository: {repo_path}")
    
    store = GraphStore()
    if not store.is_connected():
        logger.error("❌ Cannot build graph: Neo4j is not reachable. Please start Neo4j.")
        return

    if wipe_existing:
        logger.info("Clearing existing graph data...")
        store.clear_database()

    ingestor = FileIngestor(repo_path=repo_path)
    extractor = GraphExtractor(provider=provider)
    
    documents = ingestor.load_repo()
    if not documents:
        logger.warning(f"No code files found in '{repo_path}'. Make sure files have supported extensions (.py, .js, .ts, etc.)")
        store.close()
        return

    logger.info(f"Found {len(documents)} source files. Parsing entities & relationships...")

    for doc in documents:
        file_path = doc['path']
        content = doc['content']
        logger.info(f"Analyzing: {file_path}")
        
        chunks = ingestor.chunk_code(content)
        for chunk in chunks:
            nodes_and_rels = extractor.extract_and_store(chunk)
            
            # Link entities to their parent File node
            file_link_data = []
            for item in nodes_and_rels:
                file_link_data.append({
                    "source": file_path,
                    "source_type": "File",
                    "target": item.get('source', ''),
                    "target_type": item.get('source_type', 'Entity'),
                    "relationship": "CONTAINS"
                })
            
            store.add_graph_chunk(file_link_data)
            store.add_graph_chunk(nodes_and_rels)
            
    store.close()
    logger.info("🎉 Code Graph Build Complete!")


def chat_loop(provider: str = None):
    """
    Interactive loop for the user to explore the codebase graph.
    """
    print("\n" + "="*56)
    print(f"🤖 Code GraphRAG System Ready! (Provider: {provider or Config.DEFAULT_PROVIDER})")
    print("Ask any architectural or relational questions about the codebase.")
    print("Type 'exit' or 'quit' to stop.")
    print("="*56 + "\n")
    
    rag = RAGPipeline(provider=provider)
    
    try:
        while True:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                break
                
            response = rag.get_answer(user_input)
            print(f"\nAI: {response}\n")
    finally:
        rag.close()


def main():
    parser = argparse.ArgumentParser(
        description="CodeGraph-RAG: Graph-Augmented Codebase Intelligence"
    )
    parser.add_argument(
        "--repo", "-r",
        type=str,
        default="data",
        help="Path to repository to ingest (default: 'data')"
    )
    parser.add_argument(
        "--provider", "-p",
        choices=["gemini", "groq"],
        default=None,
        help="LLM provider (gemini or groq; defaults to env config)"
    )
    parser.add_argument(
        "--build", "-b",
        action="store_true",
        help="Ingest and build the Neo4j knowledge graph"
    )
    parser.add_argument(
        "--wipe", "-w",
        action="store_true",
        help="Wipe existing graph before building"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Execute a one-shot query from CLI instead of interactive chat"
    )

    args = parser.parse_args()

    # Direct query mode
    if args.query:
        rag = RAGPipeline(provider=args.provider)
        answer = rag.get_answer(args.query)
        print(f"\nAnswer:\n{answer}")
        rag.close()
        return

    # Direct build mode
    if args.build:
        build_knowledge_graph(repo_path=args.repo, provider=args.provider, wipe_existing=args.wipe)
        return

    # Interactive mode prompt if no flags provided
    print("="*56)
    print("   CodeGraph-RAG: Codebase Graph Explorer")
    print("="*56)
    mode = input("Select mode: (1) Build Knowledge Graph, (2) Interactive Chat [1/2]: ").strip()
    
    if mode == "1":
        wipe_choice = input("Wipe existing Neo4j database first? (y/n) [n]: ").strip().lower()
        build_knowledge_graph(repo_path=args.repo, provider=args.provider, wipe_existing=(wipe_choice == 'y'))
        chat_choice = input("Launch chat loop now? (y/n) [y]: ").strip().lower()
        if chat_choice != 'n':
            chat_loop(provider=args.provider)
    elif mode == "2":
        chat_loop(provider=args.provider)
    else:
        print("Invalid selection. Exiting.")


if __name__ == "__main__":
    main()
