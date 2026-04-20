"""Configuration management for TikTok Ads MCP Server"""

import os

class TikTokConfig:
    """Configuration class for TikTok Business API"""
    
    # TikTok API Configuration
    APP_ID: str = os.getenv("TIKTOK_APP_ID", "")
    SECRET: str = os.getenv("TIKTOK_SECRET", "")
    ACCESS_TOKEN: str = os.getenv("TIKTOK_ACCESS_TOKEN", "")
    ADVERTISER_ID: str = os.getenv("TIKTOK_ADVERTISER_ID", "")
    SANDBOX: bool = os.getenv("TIKTOK_SANDBOX", "false").lower() == "true"
    
    # API URLs
    BASE_URL: str = "https://business-api.tiktok.com/open_api" if not SANDBOX else "https://sandbox-ads.tiktok.com/open_api"
    API_VERSION: str = "v1.3"
    
    # Request Configuration
    REQUEST_TIMEOUT: int = int(os.getenv("TIKTOK_REQUEST_TIMEOUT", "30"))  # seconds
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that all required credentials are present"""
        required_fields = [cls.APP_ID, cls.SECRET, cls.ACCESS_TOKEN]
        return all(field.strip() for field in required_fields)
    
    @classmethod
    def get_missing_credentials(cls) -> list[str]:
        """Get list of missing credential fields"""
        missing = []
        if not cls.APP_ID.strip():
            missing.append("TIKTOK_APP_ID")
        if not cls.SECRET.strip():
            missing.append("TIKTOK_SECRET")
        if not cls.ACCESS_TOKEN.strip():
            missing.append("TIKTOK_ACCESS_TOKEN")
        return missing

# Global config instance
config = TikTokConfig() 