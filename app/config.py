import os
from dataclasses import dataclass

@dataclass
class Settings:
    USE_MOCK_DATA: bool = (os.getenv("USE_MOCK_DATA", "true").lower() == "true")

    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: str | None = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")

    AZURE_SUBSCRIPTION_ID: str | None = os.getenv("AZURE_SUBSCRIPTION_ID", "mock-subscription")
    AZURE_TENANT_ID: str | None = os.getenv("AZURE_TENANT_ID", "mock-tenant")
    AZURE_CLIENT_ID: str | None = os.getenv("AZURE_CLIENT_ID", "mock-client")
    AZURE_CLIENT_SECRET: str | None = os.getenv("AZURE_CLIENT_SECRET", "mock-secret")

    AWS_ALERT_THRESHOLD: float = float(os.getenv("AWS_ALERT_THRESHOLD", "450"))
    AZURE_ALERT_THRESHOLD: float = float(os.getenv("AZURE_ALERT_THRESHOLD", "350"))

settings = Settings()
