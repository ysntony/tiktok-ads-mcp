"""Get Campaigns Tool"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

async def get_campaigns(client, advertiser_id: str, filters: dict | None = None, **kwargs) -> list[dict[str, Any]]:
    """Get campaigns for an advertiser"""
    params = {
        'advertiser_id': advertiser_id
    }
    
    # Add filters if provided
    if filters:
        if 'campaign_ids' in filters:
            params['campaign_ids'] = json.dumps(filters['campaign_ids'])
        # Note: status filter removed as it's not supported by the API
    
    response = await client._make_request('GET', 'campaign/get/', params)
    campaigns = response.get('data', {}).get('list', [])

    return [
        {
            "campaign_id": camp.get("campaign_id"),
            "campaign_name": camp.get("campaign_name", "Unknown"),
            "advertiser_id": camp.get("advertiser_id"),
            "objective": camp.get("objective", "Unknown"),
            "objective_type": camp.get("objective_type", "Unknown"),
            "budget": float(camp.get("budget", 0)),
            "budget_mode": camp.get("budget_mode", "Unknown"),
            "operation_status": camp.get("operation_status", "Unknown"),
            "secondary_status": camp.get("secondary_status", "Unknown"),
            "campaign_type": camp.get("campaign_type", "REGULAR_CAMPAIGN"),
            "is_smart_performance_campaign": camp.get("is_smart_performance_campaign", False),
            "is_new_structure": camp.get("is_new_structure", False),
            "roas_bid": float(camp.get("roas_bid", 0)),
            "deep_bid_type": camp.get("deep_bid_type"),
            "create_time": camp.get("create_time"),
            "modify_time": camp.get("modify_time")
        }
        for camp in campaigns
    ]