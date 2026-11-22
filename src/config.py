import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """
    Central configuration class.
    Validates environment variables on demand to allow flexible deployment.
    """
    
    # 1. Google Gemini Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # 2. Neo4j Database Configuration
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
    
    # 3. Model Configuration
    DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
    GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GROQ_MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

    @classmethod
    def validate(cls, provider: str = None):
        """
        Validates required keys depending on the active LLM provider.
        """
        active_provider = (provider or cls.DEFAULT_PROVIDER).lower()
        missing_keys = []
        
        if active_provider == "gemini":
            if not cls.GOOGLE_API_KEY or cls.GOOGLE_API_KEY.startswith("your_"):
                missing_keys.append("GOOGLE_API_KEY")
        elif active_provider == "groq":
            if not cls.GROQ_API_KEY or cls.GROQ_API_KEY.startswith("your_"):
                missing_keys.append("GROQ_API_KEY")
                
        if not cls.NEO4J_URI:
            missing_keys.append("NEO4J_URI")
            
        if missing_keys:
            raise ValueError(
                f"Missing required configuration keys for provider '{active_provider}': "
                f"{', '.join(missing_keys)}. Please check your .env file."
            )
        return True
