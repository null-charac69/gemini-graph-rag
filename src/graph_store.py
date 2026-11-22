import re
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add project root to path to allow imports when running directly
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from neo4j import GraphDatabase
from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _sanitize_identifier(identifier: str, default: str = "Entity") -> str:
    """Sanitizes node labels or relationship names for safe Cypher execution."""
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', str(identifier).strip())
    return cleaned if cleaned else default


class GraphStore:
    def __init__(self):
        """
        Initialize the Neo4j driver using credentials from Config.
        """
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
            )
            self.verify_connection()
        except Exception as e:
            logger.warning(
                f"⚠️ Could not establish connection to Neo4j at {Config.NEO4J_URI}: {e}\n"
                f"Tip: Run Neo4j locally with Docker:\n"
                f"  docker compose up -d\n"
                f"  or: docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest"
            )

    def verify_connection(self) -> bool:
        """Simple check to ensure we can talk to the database."""
        if not self.driver:
            return False
        try:
            self.driver.verify_connectivity()
            logger.info("✅ Successfully connected to Neo4j Graph Database!")
            return True
        except Exception as e:
            logger.warning(f"Connection verification failed: {e}")
            return False

    def is_connected(self) -> bool:
        return self.driver is not None

    def close(self):
        """Close driver connections."""
        if self.driver:
            self.driver.close()

    def add_graph_chunk(self, nodes_and_rels: List[Dict[str, Any]]):
        """
        Persists extracted code entities and relationships into Neo4j.
        Sanitizes labels and executes updates within an atomic session.
        """
        if not self.driver or not nodes_and_rels:
            return

        with self.driver.session() as session:
            for item in nodes_and_rels:
                try:
                    source_name = str(item.get('source', '')).strip()
                    target_name = str(item.get('target', '')).strip()
                    if not source_name or not target_name:
                        continue

                    source_type = _sanitize_identifier(item.get('source_type', 'Entity'))
                    target_type = _sanitize_identifier(item.get('target_type', 'Entity'))
                    rel_type = _sanitize_identifier(item.get('relationship', 'RELATES_TO')).upper()

                    # Cypher query with sanitized labels and parameterized names
                    cypher_query = (
                        f"MERGE (s:{source_type} {{name: $source_name}}) "
                        f"MERGE (t:{target_type} {{name: $target_name}}) "
                        f"MERGE (s)-[:{rel_type}]->(t)"
                    )
                    session.run(
                        cypher_query,
                        source_name=source_name,
                        target_name=target_name
                    )
                except Exception as e:
                    logger.debug(f"Error persisting relationship {item}: {e}")

    def clear_database(self):
        """DANGEROUS: Deletes all nodes and relationships in the database."""
        if not self.driver:
            return
        try:
            with self.driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                logger.info("🗑️ Neo4j Database cleared successfully.")
        except Exception as e:
            logger.error(f"Failed to clear database: {e}")

    def query_graph(self, cypher_query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Run a generic Cypher query and return a list of record dicts.
        """
        if not self.driver:
            return []
        params = params or {}
        try:
            with self.driver.session() as session:
                result = session.run(cypher_query, params)
                return [record.data() for record in result]
        except Exception as e:
            logger.error(f"Cypher query failed ({cypher_query}): {e}")
            return []
