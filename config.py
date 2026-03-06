"""
Configuration management for Data Alchemy pipeline.
Centralizes all environment variables and configuration constants.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class PipelineConfig:
    """Pipeline configuration container with validation."""
    
    # Firebase Configuration
    firebase_credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")
    firestore_collection: str = os.getenv("FIRESTORE_COLLECTION", "data_alchemy_jobs")
    
    # Processing Configuration
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    retry_delay: int = int(os.getenv("RETRY_DELAY", "5"))
    
    # Model Configuration
    deepseek_api_url: Optional[str] = os.getenv("DEEPSEEK_API_URL")
    deepseek_api_key: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    model_timeout: int = int(os.getenv("MODEL_TIMEOUT", "30"))
    
    # Validation
    def validate(self) -> None:
        """Validate configuration and raise informative errors."""
        if not os.path.exists(self.firebase_credentials_path):
            raise FileNotFoundError(
                f"Firebase credentials not found at: {self.firebase_credentials_path}"
            )
        
        if not self.deepseek_api_url and os.getenv("REQUIRE_MODEL", "true").lower() == "true":
            raise ValueError("DeepSeek API URL is required when model processing is enabled")
    
    @property
    def model_enabled(self) -> bool:
        """Check if model processing is enabled."""
        return bool(self.deepseek_api_url and self.deepseek_api_key)

# Global configuration instance
config = PipelineConfig()