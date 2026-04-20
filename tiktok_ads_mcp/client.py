"""TikTok Ads API Client for MCP Server"""

import httpx
import json
import logging
from typing import Any
from urllib.parse import urlencode
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import config

# Set up logging
logger = logging.getLogger(__name__)

class TikTokAdsClient:
    """TikTok Business API client for campaign operations."""
    
    def __init__(self):
        """Initialize TikTok API client"""
        # Validate credentials on initialization
        if not config.validate_credentials():
            missing = config.get_missing_credentials()
            raise Exception(
                f"Missing required credentials: {', '.join(missing)}. "
                f"Please check your configuration and ensure all required fields are set."
            )
        
        self.app_id = config.APP_ID
        self.secret = config.SECRET
        self.access_token = config.ACCESS_TOKEN
        self.base_url = config.BASE_URL
        self.api_version = config.API_VERSION
        self.request_timeout = config.REQUEST_TIMEOUT
        
        logger.info("TikTok API client initialized")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def _make_request(self, method: str, endpoint: str, params: dict | None = None,
                     data: dict | None = None) -> dict[str, Any]:
        """Make HTTP request to TikTok API with proper authentication handling"""
        
        # Prepare parameters
        if params is None:
            params = {}
        
        # Add app_id and secret ONLY for oauth2 endpoints
        if 'oauth2' in endpoint:
            params.update({
                'app_id': self.app_id,
                'secret': self.secret
            })
        
        # Construct URL
        endpoint = endpoint.lstrip('/')
        if params:
            query_string = urlencode(params)
            url = f"{self.base_url}/{self.api_version}/{endpoint}?{query_string}"
        else:
            url = f"{self.base_url}/{self.api_version}/{endpoint}"
        
        headers = {
            'Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
        
        safe_headers = {k: ('***REDACTED***' if k == 'Access-Token' else v) for k, v in headers.items()}
        logger.debug(f"Making {method} request to {url}")
        logger.debug(f"Parameters: {params}")
        logger.debug(f"Headers: {safe_headers}")

        async with httpx.AsyncClient(timeout=self.request_timeout) as client:
            if method == 'GET':
                response = await client.get(url, headers=headers)
            elif method == 'POST':
                response = await client.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            logger.debug(f"Response status: {response.status_code}")

            if response.status_code == 401:
                raise Exception("Invalid access token or credentials")
            elif response.status_code == 403:
                raise Exception("Access forbidden - check your API permissions")
            elif response.status_code >= 400:
                response.raise_for_status()

            try:
                result = response.json()
            except json.JSONDecodeError:
                raise Exception(f"Invalid JSON response: {response.text}")

            if result.get('code') != 0:
                error_msg = result.get('message', 'Unknown API error')
                raise Exception(f"TikTok API error {result.get('code')}: {error_msg}")

            return result