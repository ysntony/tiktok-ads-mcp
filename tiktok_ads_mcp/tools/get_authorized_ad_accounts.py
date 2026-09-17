"""Get Authorized Ad Accounts Tool"""

import logging
from typing import Any

from ._utils import preserve_item

logger = logging.getLogger(__name__)

async def get_authorized_ad_accounts(client, **kwargs) -> list[dict[str, Any]]:
    """Get all authorized ad accounts"""
    response = await client._make_request('GET', 'oauth2/advertiser/get/')
    advertisers = response.get('data', {}).get('list', [])

    normalized = []
    for advertiser in advertisers:
        item = preserve_item(advertiser)
        for field, default in {
            "advertiser_name": "Unknown", "status": "Unknown", "company": "",
            "country": "", "currency": "", "timezone": "",
        }.items():
            item.setdefault(field, default)
        normalized.append(item)
    return normalized
