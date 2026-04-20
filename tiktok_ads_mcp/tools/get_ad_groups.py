"""Get Ad Groups Tool"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

async def get_ad_groups(client, advertiser_id: str, campaign_id: str | None = None, filters: dict | None = None, page: int = 1, page_size: int = 10, **kwargs) -> list[dict[str, Any]]:
    """Get ad groups for a specific advertiser with optional filtering"""
    
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
        if campaign_id:
            existing = filters.get('campaign_ids', [])
            filters['campaign_ids'] = list(existing) + [campaign_id] if isinstance(existing, list) else [campaign_id]
        params['filtering'] = json.dumps(filters)
    elif campaign_id:
        params['filtering'] = json.dumps({'campaign_ids': [campaign_id]})
    
    response = await client._make_request('GET', 'adgroup/get/', params)
    ad_groups = response.get('data', {}).get('list', [])

    return [
        {
            "adgroup_id": adgroup.get("adgroup_id"),
            "adgroup_name": adgroup.get("adgroup_name", "Unknown"),
            "campaign_id": adgroup.get("campaign_id"),
            "campaign_name": adgroup.get("campaign_name", "Unknown"),
            "advertiser_id": adgroup.get("advertiser_id"),
            "budget": float(adgroup.get("budget", 0)),
            "budget_mode": adgroup.get("budget_mode", "Unknown"),
            "operation_status": adgroup.get("operation_status", "Unknown"),
            "secondary_status": adgroup.get("secondary_status", "Unknown"),
            "optimization_goal": adgroup.get("optimization_goal", "Unknown"),
            "billing_event": adgroup.get("billing_event", "Unknown"),
            "bid_type": adgroup.get("bid_type", "Unknown"),
            "bid_price": float(adgroup.get("bid_price", 0)),
            "conversion_bid_price": float(adgroup.get("conversion_bid_price", 0)),
            "deep_bid_type": adgroup.get("deep_bid_type"),
            "deep_cpa_bid": float(adgroup.get("deep_cpa_bid", 0)),
            "promotion_type": adgroup.get("promotion_type", "Unknown"),
            "creative_material_mode": adgroup.get("creative_material_mode", "Unknown"),
            "schedule_type": adgroup.get("schedule_type", "Unknown"),
            "schedule_start_time": adgroup.get("schedule_start_time"),
            "schedule_end_time": adgroup.get("schedule_end_time"),
            "pacing": adgroup.get("pacing", "Unknown"),
            "gender": adgroup.get("gender", "Unknown"),
            "age_groups": adgroup.get("age_groups"),
            "location_ids": adgroup.get("location_ids", []),
            "placements": adgroup.get("placements", []),
            "operating_systems": adgroup.get("operating_systems", []),
            "languages": adgroup.get("languages", []),
            "audience_ids": adgroup.get("audience_ids", []),
            "excluded_audience_ids": adgroup.get("excluded_audience_ids", []),
            "interest_category_ids": adgroup.get("interest_category_ids", []),
            "interest_keyword_ids": adgroup.get("interest_keyword_ids", []),
            "auto_targeting_enabled": adgroup.get("auto_targeting_enabled", False),
            "is_new_structure": adgroup.get("is_new_structure", False),
            "is_hfss": adgroup.get("is_hfss", False),
            "skip_learning_phase": adgroup.get("skip_learning_phase", False),
            "search_result_enabled": adgroup.get("search_result_enabled", False),
            "inventory_filter_enabled": adgroup.get("inventory_filter_enabled", False),
            "video_download_disabled": adgroup.get("video_download_disabled", False),
            "comment_disabled": adgroup.get("comment_disabled", False),
            "share_disabled": adgroup.get("share_disabled", False),
            "brand_safety_type": adgroup.get("brand_safety_type", "Unknown"),
            "brand_safety_partner": adgroup.get("brand_safety_partner"),
            "pixel_id": adgroup.get("pixel_id"),
            "app_id": adgroup.get("app_id"),
            "app_download_url": adgroup.get("app_download_url"),
            "app_type": adgroup.get("app_type"),
            "category_id": adgroup.get("category_id"),
            "create_time": adgroup.get("create_time"),
            "modify_time": adgroup.get("modify_time")
        }
        for adgroup in ad_groups
    ]