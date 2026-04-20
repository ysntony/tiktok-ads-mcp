"""Get Authorized Ad Accounts Tool"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

async def get_authorized_ad_accounts(client, **kwargs) -> list[dict[str, Any]]:
    """Get all authorized ad accounts"""
    response = await client._make_request('GET', 'oauth2/advertiser/get/')
    advertisers = response.get('data', {}).get('list', [])

    return [
        {
            "advertiser_id": adv.get("advertiser_id"),
            "advertiser_name": adv.get("advertiser_name", "Unknown"),
            "status": adv.get("status", "Unknown"),
            "company": adv.get("company", ""),
            "country": adv.get("country", ""),
            "currency": adv.get("currency", ""),
            "timezone": adv.get("timezone", "")
        }
        for adv in advertisers
    ]