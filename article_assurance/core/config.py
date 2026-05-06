from pydantic_settings import BaseSettings#from pydantic import BaseSettings


class AssuranceConfig(BaseSettings):

    APIVOID_API_KEY: str = ""

    TRUST_VALID_THRESHOLD: float = 0.75
    TRUST_UNCERTAIN_THRESHOLD: float = 0.50

    PUBLISHER_WEIGHT: float = 0.30
    PROVENANCE_WEIGHT: float = 0.25
    CORROBORATION_WEIGHT: float = 0.45

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    NLI_MODEL: str = "cross-encoder/nli-deberta-v3-small"

    class Config:
        env_file = ".env"