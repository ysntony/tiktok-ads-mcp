"""Get Ads Tool"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

async def get_ads(client, advertiser_id: str, adgroup_id: str | None = None, filters: dict | None = None, page: int = 1, page_size: int = 10, **kwargs) -> list[dict[str, Any]]:
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
    ads = response.get('data', {}).get('list', [])

    return [
        {
            "ad_id": ad.get("ad_id"),
            "ad_name": ad.get("ad_name", "Unknown"),
            "adgroup_id": ad.get("adgroup_id"),
            "adgroup_name": ad.get("adgroup_name", "Unknown"),
            "campaign_id": ad.get("campaign_id"),
            "campaign_name": ad.get("campaign_name", "Unknown"),
            "advertiser_id": ad.get("advertiser_id"),
            "operation_status": ad.get("operation_status", "Unknown"),
            "secondary_status": ad.get("secondary_status", "Unknown"),
            "ad_format": ad.get("ad_format", "Unknown"),
            "creative_type": ad.get("creative_type"),
            "ad_text": ad.get("ad_text", ""),
            "ad_texts": ad.get("ad_texts"),
            "call_to_action": ad.get("call_to_action", ""),
            "call_to_action_id": ad.get("call_to_action_id"),
            "landing_page_url": ad.get("landing_page_url", ""),
            "landing_page_urls": ad.get("landing_page_urls"),
            "deeplink": ad.get("deeplink", ""),
            "deeplink_type": ad.get("deeplink_type", "Unknown"),
            "video_id": ad.get("video_id"),
            "image_ids": ad.get("image_ids", []),
            "playable_url": ad.get("playable_url", ""),
            "profile_image_url": ad.get("profile_image_url", ""),
            "avatar_icon_web_uri": ad.get("avatar_icon_web_uri", ""),
            "display_name": ad.get("display_name", ""),
            "identity_type": ad.get("identity_type", "Unknown"),
            "identity_id": ad.get("identity_id"),
            "app_name": ad.get("app_name", ""),
            "page_id": ad.get("page_id"),
            "card_id": ad.get("card_id"),
            "optimization_event": ad.get("optimization_event"),
            "tracking_pixel_id": ad.get("tracking_pixel_id", 0),
            "click_tracking_url": ad.get("click_tracking_url"),
            "impression_tracking_url": ad.get("impression_tracking_url"),
            "viewability_vast_url": ad.get("viewability_vast_url"),
            "brand_safety_vast_url": ad.get("brand_safety_vast_url"),
            "brand_safety_postbid_partner": ad.get("brand_safety_postbid_partner", "Unknown"),
            "viewability_postbid_partner": ad.get("viewability_postbid_partner", "Unknown"),
            "fallback_type": ad.get("fallback_type", "Unknown"),
            "is_aco": ad.get("is_aco", False),
            "is_new_structure": ad.get("is_new_structure", False),
            "creative_authorized": ad.get("creative_authorized", False),
            "vast_moat_enabled": ad.get("vast_moat_enabled", False),
            "create_time": ad.get("create_time"),
            "modify_time": ad.get("modify_time")
        }
        for ad in ads
    ]