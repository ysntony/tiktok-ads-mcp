"""Get Ad Groups Tool"""

import json
import logging
from typing import Any

from ._utils import as_float, preserve_item, with_metadata

logger = logging.getLogger(__name__)

async def get_ad_groups(client, advertiser_id: str, campaign_id: str | None = None, filters: dict | None = None, page: int = 1, page_size: int = 10, include_metadata: bool = False, **kwargs) -> list[dict[str, Any]] | dict[str, Any]:
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
    data = response.get('data', {})
    ad_groups = data.get('list', [])

    normalized = []
    for adgroup in ad_groups:
        item = preserve_item(adgroup)
        for field, default in {
            "adgroup_name": "Unknown", "campaign_name": "Unknown", "budget_mode": "Unknown",
            "operation_status": "Unknown", "secondary_status": "Unknown", "optimization_goal": "Unknown",
            "billing_event": "Unknown", "bid_type": "Unknown", "promotion_type": "Unknown",
            "creative_material_mode": "Unknown", "schedule_type": "Unknown", "pacing": "Unknown",
            "gender": "Unknown", "brand_safety_type": "Unknown",
        }.items():
            item.setdefault(field, default)
        for field in ("budget", "bid_price", "conversion_bid_price", "deep_cpa_bid"):
            item[field] = as_float(item.get(field))
        normalized.append(item)
    return with_metadata(normalized, data, include_metadata)
