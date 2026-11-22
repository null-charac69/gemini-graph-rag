"""
Groq LLM Service Wrapper (delegates to unified LLMService with provider='groq').
"""
from src.llm_service import LLMService as UnifiedLLMService

class LLMService(UnifiedLLMService):
    def __init__(self):
        super().__init__(provider="groq")
