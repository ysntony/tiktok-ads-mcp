"""Get Ads Tool"""

import json
import logging
from typing import Any

from ._utils import as_float, preserve_item, with_metadata

logger = logging.getLogger(__name__)

async def get_ads(client, advertiser_id: str, adgroup_id: str | None = None, filters: dict | None = None, page: int = 1, page_size: int = 10, include_metadata: bool = False, **kwargs) -> list[dict[str, Any]] | dict[str, Any]:
    """Get ads for a specific advertiser with optional filtering"""
    
    if not advertiser_id:
        raise ValueError("advertiser_id is required")
    
    # Validate pagination parameters
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1 or page_size > 1000:
        raise ValueError("page_size must be between 1 and 1000")
    
    # Prepare base parameters
    params = {
        'advertiser_id': advertiser_id,
        'page': page,
        'page_size': page_size
    }
    
    # Add filtering if provided
    if filters:
        filters = dict(filters)
        if adgroup_id:
            existing = filters.get('adgroup_ids', [])
            filters['adgroup_ids'] = list(existing) + [adgroup_id] if isinstance(existing, list) else [adgroup_id]
        params['filtering'] = json.dumps(filters)
    elif adgroup_id:
        params['filtering'] = json.dumps({'adgroup_ids': [adgroup_id]})
    
    response = await client._make_request('GET', 'ad/get/', params)
    data = response.get('data', {})
    ads = data.get('list', [])

    normalized = []
    for ad in ads:
        item = preserve_item(ad)
        for field, default in {
            "ad_name": "Unknown", "adgroup_name": "Unknown", "campaign_name": "Unknown",
            "operation_status": "Unknown", "secondary_status": "Unknown", "ad_format": "Unknown",
            "ad_text": "", "call_to_action": "", "landing_page_url": "", "deeplink": "",
            "deeplink_type": "Unknown", "image_ids": [], "playable_url": "", "profile_image_url": "",
            "avatar_icon_web_uri": "", "display_name": "", "identity_type": "Unknown", "app_name": "",
            "brand_safety_postbid_partner": "Unknown", "viewability_postbid_partner": "Unknown",
            "fallback_type": "Unknown", "is_aco": False, "is_new_structure": False,
            "creative_authorized": False, "vast_moat_enabled": False,
        }.items():
            item.setdefault(field, default)
        if "tracking_pixel_id" not in item:
            item["tracking_pixel_id"] = 0
        normalized.append(item)
    return with_metadata(normalized, data, include_metadata)
