"""Get Business Centers Tool"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

async def get_business_centers(client, bc_id: str | None = None, page: int = 1, page_size: int = 10, **kwargs) -> list[dict[str, Any]]:
    """Get business centers accessible by the current access token"""
    
    # Validate parameters
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1 or page_size > 50:
        raise ValueError("page_size must be between 1 and 50")
    
    # Prepare parameters
    params = {
        'page': page,
        'page_size': page_size
    }
    
    # Add bc_id if provided
    if bc_id:
        params['bc_id'] = bc_id
    
    response = await client._make_request('GET', 'bc/get/', params)
    business_centers = response.get('data', {}).get('list', [])

    return [
        {
            "bc_id": bc.get("bc_id"),
            "name": bc.get("name", "Unknown"),
            "company": bc.get("company", ""),
            "currency": bc.get("currency", ""),
            "registered_area": bc.get("registered_area", ""),
            "status": bc.get("status", "Unknown"),
            "timezone": bc.get("timezone", ""),
            "type": bc.get("type", "Unknown"),
            "user_role": bc.get("user_role", "Unknown"),
            "finance_role": bc.get("finance_role"),
            "ext_user_role": bc.get("ext_user_role")
        }
        for bc in business_centers
    ]