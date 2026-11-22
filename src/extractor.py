import logging
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add project root to path to allow imports when running directly
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.llm_service import LLMService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphExtractor:
    """
    Extracts structured relationships (Classes, Functions, Calls, Imports)
    from source code snippets using LLM static analysis.
    """
    def __init__(self, llm_service: Optional[LLMService] = None, provider: Optional[str] = None):
        self.llm = llm_service or LLMService(provider=provider)

    def extract_and_store(self, text_chunk: str) -> List[Dict[str, Any]]:
        """
        Extracts entities and relationships from a code snippet.
        Returns a list of relationship dictionaries.
        """
        prompt = f"""You are an expert Static Code Analysis engine. Your objective is to map the topological graph of the provided Source Code.

**Rules:**
1. Identify code entities: Class, Function, File, Library, Variable.
2. Identify directed relationships:
    - DEFINES (File/Class defines Function/Method)
    - CALLS (Function calls Function)
    - IMPORTS (File/Module imports Library/Symbol)
    - INHERITS (Class inherits from BaseClass)
3. Return ONLY a valid JSON list of objects matching the schema:
   [
     {{"source": "name", "source_type": "Function", "target": "other", "target_type": "Library", "relationship": "IMPORTS"}}
   ]

**Source Code Snippet:**
```
{text_chunk}
```

**JSON Output:**"""

        logger.debug("Extracting entities from code chunk...")
        result = self.llm.get_json_response(prompt)
        return result if isinstance(result, list) else []
