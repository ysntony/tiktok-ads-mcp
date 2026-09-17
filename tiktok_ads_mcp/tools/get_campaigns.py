"""Get Campaigns Tool"""

import json
import logging
from typing import Any

from ._utils import as_float, preserve_item, with_metadata

logger = logging.getLogger(__name__)

async def get_campaigns(
    client,
    advertiser_id: str,
    filters: dict | None = None,
    page: int = 1,
    page_size: int = 10,
    include_metadata: bool = False,
    **kwargs,
) -> list[dict[str, Any]] | dict[str, Any]:
    """Get campaigns for an advertiser"""
    if not advertiser_id:
        raise ValueError("advertiser_id is required")
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1 or page_size > 1000:
        raise ValueError("page_size must be between 1 and 1000")

    params = {
        'advertiser_id': advertiser_id,
        'page': page,
        'page_size': page_size,
    }

    if filters:
        # TikTok v1.3 expects all campaign filters inside one filtering object.
        filtering = dict(filters)
        params['filtering'] = json.dumps(filtering)

    response = await client._make_request('GET', 'campaign/get/', params)
    data = response.get('data', {})
    campaigns = data.get('list', [])

    normalized = []
    for campaign in campaigns:
        item = preserve_item(campaign)
        item.setdefault("campaign_name", "Unknown")
        item.setdefault("objective", "Unknown")
        item.setdefault("objective_type", "Unknown")
        item.setdefault("budget_mode", "Unknown")
        item.setdefault("operation_status", "Unknown")
        item.setdefault("secondary_status", "Unknown")
        item.setdefault("campaign_type", "REGULAR_CAMPAIGN")
        item.setdefault("is_smart_performance_campaign", False)
        item.setdefault("is_new_structure", False)
        item["budget"] = as_float(item.get("budget"))
        item["roas_bid"] = as_float(item.get("roas_bid"))
        normalized.append(item)

    return with_metadata(normalized, data, include_metadata)
