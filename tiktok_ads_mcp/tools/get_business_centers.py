"""Get Business Centers Tool"""

import logging
from typing import Any

from ._utils import preserve_item, with_metadata

logger = logging.getLogger(__name__)

async def get_business_centers(client, bc_id: str | None = None, page: int = 1, page_size: int = 10, include_metadata: bool = False, **kwargs) -> list[dict[str, Any]] | dict[str, Any]:
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
    data = response.get('data', {})
    business_centers = data.get('list', [])

    normalized = []
    for center in business_centers:
        item = preserve_item(center)
        for field, default in {
            "name": "Unknown", "company": "", "currency": "", "registered_area": "",
            "status": "Unknown", "timezone": "", "type": "Unknown", "user_role": "Unknown",
        }.items():
            item.setdefault(field, default)
        normalized.append(item)
    return with_metadata(normalized, data, include_metadata)
