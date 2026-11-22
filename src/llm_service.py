import json
import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path to allow imports when running directly
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """
    Unified LLM service supporting Google Gemini and Groq.
    Provides standard generation and schema-safe JSON extraction.
    """
    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or Config.DEFAULT_PROVIDER).lower()
        self.gemini_client = None
        self.groq_client = None

        if self.provider == "gemini":
            import google.genai as genai
            self.model_name = Config.GEMINI_MODEL_NAME
            if Config.GOOGLE_API_KEY:
                try:
                    self.gemini_client = genai.Client(api_key=Config.GOOGLE_API_KEY)
                    logger.info(f"Initialized Gemini Client (model: {self.model_name})")
                except Exception as e:
                    logger.error(f"Failed to initialize Gemini: {e}")
            else:
                logger.warning("GOOGLE_API_KEY not set. Gemini generation will fail.")

        elif self.provider == "groq":
            from groq import Groq
            self.model_name = Config.GROQ_MODEL_NAME
            if Config.GROQ_API_KEY:
                try:
                    self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
                    logger.info(f"Initialized Groq Client (model: {self.model_name})")
                except Exception as e:
                    logger.error(f"Failed to initialize Groq: {e}")
            else:
                logger.warning("GROQ_API_KEY not set. Groq generation will fail.")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}. Use 'gemini' or 'groq'.")

    def get_response(self, prompt: str) -> str:
        """
        Standard text generation for answering user questions.
        """
        try:
            if self.provider == "gemini":
                if not self.gemini_client:
                    return "Error: Gemini client not initialized. Check your GOOGLE_API_KEY in .env."
                response = self.gemini_client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                return response.text.strip() if response and response.text else "No response generated."

            elif self.provider == "groq":
                if not self.groq_client:
                    return "Error: Groq client not initialized. Check your GROQ_API_KEY in .env."
                chat_completion = self.groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert software engineer analyzing a codebase knowledge graph."},
                        {"role": "user", "content": prompt}
                    ],
                    model=self.model_name,
                    temperature=0.2,
                )
                return chat_completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"LLM Generation error with provider '{self.provider}': {e}")
            return f"I encountered an error generating an answer ({e})."

    def get_json_response(self, prompt: str) -> Union[List, Dict]:
        """
        Generates content and extracts a valid JSON structure (list or dict).
        Handles markdown fences, trailing commas, and raw outputs.
        """
        raw_text = self.get_response(prompt)
        clean_text = self._clean_json_text(raw_text)
        
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            # Fallback: attempt regex extraction of array or object
            array_match = re.search(r'\[\s*{.*}\s*\]', raw_text, re.DOTALL)
            if array_match:
                try:
                    return json.loads(array_match.group(0))
                except Exception:
                    pass
            logger.warning(f"Failed to parse JSON response. Raw snippet: {raw_text[:120]}")
            return []

    def _clean_json_text(self, text: str) -> str:
        """
        Strips markdown code fences (```json ... ```) from LLM output.
        """
        text = text.strip()
        match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text


# Backwards compatibility alias
from typing import Union
