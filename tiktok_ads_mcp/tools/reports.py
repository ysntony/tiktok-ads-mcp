"""Get Reports Tool"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

async def get_reports(client, advertiser_id: str | None = None, advertiser_ids: list[str] | None = None, bc_id: str | None = None,
                report_type: str = "BASIC", data_level: str = "AUCTION_CAMPAIGN",
                dimensions: list[str] | None = None, metrics: list[str] | None = None,
                start_date: str | None = None, end_date: str | None = None,
                filters: list[dict] | None = None, page: int = 1, page_size: int = 10,
                service_type: str = "AUCTION", query_lifetime: bool = False,
                enable_total_metrics: bool = False, multi_adv_report_in_utc_time: bool = False,
                order_field: str | None = None, order_type: str = "DESC", **kwargs) -> dict[str, Any]:
    """Get performance reports and analytics"""
    
    # Validate required parameters based on report_type
    if report_type == "BC":
        if not bc_id:
            raise ValueError("bc_id is required when report_type is BC")
    else:
        if not advertiser_id and not advertiser_ids:
            raise ValueError("advertiser_id or advertiser_ids is required when report_type is not BC")
        if advertiser_id and advertiser_ids:
            logger.warning("Both advertiser_id and advertiser_ids provided, advertiser_id will be ignored")
    
    # Validate pagination parameters
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1 or page_size > 1000:
        raise ValueError("page_size must be between 1 and 1000")
    
    # Validate date parameters
    if not query_lifetime:
        if not start_date or not end_date:
            raise ValueError("start_date and end_date are required when query_lifetime is False")
    
    # Prepare base parameters
    params = {
        'report_type': report_type,
        'page': page,
        'page_size': page_size
    }
    
    # Add advertiser/business center parameters
    if report_type == "BC":
        params['bc_id'] = bc_id
    else:
        if advertiser_ids:
            params['advertiser_ids'] = json.dumps(advertiser_ids)
        else:
            params['advertiser_id'] = advertiser_id
        params['service_type'] = service_type
        params['data_level'] = data_level
    
    # Add dimensions
    if dimensions:
        params['dimensions'] = json.dumps(dimensions)
    
    # Add metrics
    if metrics:
        params['metrics'] = json.dumps(metrics)
    
    # Add date parameters
    if not query_lifetime:
        params['start_date'] = start_date
        params['end_date'] = end_date
    
    # Add query_lifetime
    if query_lifetime:
        params['query_lifetime'] = query_lifetime
    
    # Add filtering
    if filters:
        params['filtering'] = json.dumps(filters)
    
    # Add optional parameters
    if enable_total_metrics:
        params['enable_total_metrics'] = enable_total_metrics
    
    if multi_adv_report_in_utc_time:
        params['multi_adv_report_in_utc_time'] = multi_adv_report_in_utc_time
    
    if order_field:
        params['order_field'] = order_field
    
    if order_type:
        params['order_type'] = order_type
    
    response = await client._make_request('GET', 'report/integrated/get/', params)
    data = response.get('data', {})

    return {
        "report_type": report_type,
        "data_level": data_level if report_type != "BC" else None,
        "total_metrics": data.get("total_metrics"),
        "page_info": data.get("page_info", {}),
        "list": [
            {
                "dimensions": item.get("dimensions", {}),
                "metrics": item.get("metrics", {})
            }
            for item in data.get("list", [])
        ]
    }