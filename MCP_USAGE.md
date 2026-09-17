# TikTok Ads MCP Usage Guide

This guide provides comprehensive documentation for using the TikTok Ads MCP (Model Context Protocol) server with all available tools.

## Table of Contents

1. [Overview](#overview)
2. [Setup and Configuration](#setup-and-configuration)
3. [Available Tools](#available-tools)
4. [Tool Reference](#tool-reference)
5. [Examples](#examples)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)

## Overview

The TikTok Ads MCP provides a comprehensive interface to the TikTok Business API, allowing you to:
- Retrieve business centers and advertiser accounts
- Manage campaigns, ad groups, and ads
- Generate detailed performance reports
- Access real-time advertising data

## Setup and Configuration

### 1. Install the MCP Server

```bash
# Install directly from GitHub (Recommended for latest features)
pip install git+https://github.com/ysntony/tiktok-ads-mcp.git

# OR clone and install in development mode
git clone https://github.com/ysntony/tiktok-ads-mcp.git
cd tiktok-ads-mcp
pip install -e .
```

> [!NOTE]
> This project requires **Python 3.10** or higher. Please ensure your environment is set up correctly.

### 2. Configure Cursor MCP

Add the following configuration to your `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tiktok-ads": {
      "command": "/path/to/your/python",
      "args": ["-m", "tiktok_ads_mcp"],
      "cwd": "/path/to/tiktok-ads-mcp",
      "env": {
        "TIKTOK_APP_ID": "your_app_id",
        "TIKTOK_SECRET": "your_secret",
        "TIKTOK_ACCESS_TOKEN": "your_access_token",
        "TIKTOK_ADVERTISER_ID": "your_advertiser_id"
      }
    }
  }
}
```

### 3. Environment Variables

Required environment variables:
- `TIKTOK_APP_ID`: Your TikTok app ID
- `TIKTOK_SECRET`: Your TikTok app secret
- `TIKTOK_ACCESS_TOKEN`: Your access token
- `TIKTOK_ADVERTISER_ID`: Your advertiser ID (optional)

## Available Tools

The MCP server provides 6 comprehensive tools:

1. **get_business_centers** - Retrieve business centers
2. **get_authorized_ad_accounts** - Get authorized advertiser accounts
3. **get_campaigns** - Retrieve campaigns with filtering
4. **get_ad_groups** - Get ad groups with comprehensive filtering
5. **get_ads** - Retrieve ads with detailed filtering options
6. **get_reports** - Generate performance reports and analytics

## Tool Reference

### 1. get_business_centers

Retrieves business centers accessible by the current access token.

**Parameters:**
- `bc_id` (optional): Business Center ID to filter by
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Page size 1-50 (default: 10)

**Example:**
```json
{
  "bc_id": "",
  "page": 1,
  "page_size": 10
}
```

**Response:**
```json
{
  "success": true,
  "count": 1,
  "centers": [
    {
      "bc_id": "123456789",
      "name": "My Business Center",
      "company": "My Company",
      "currency": "USD",
      "status": "ENABLE",
      "type": "NORMAL",
      "user_role": "ADMIN"
    }
  ]
}
```

### 2. get_authorized_ad_accounts

Retrieves all authorized ad accounts accessible by the current access token.

**Parameters:**
- `random_string` (optional): Dummy parameter for no-parameter tools

**Example:**
```json
{
  "random_string": "test"
}
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "advertisers": [
    {
      "advertiser_id": "7441431575776520000",
      "advertiser_name": "My Ad Account",
      "status": "STATUS_ENABLE",
      "company": "My Company",
      "country": "US",
      "currency": "USD",
      "timezone": "America/New_York"
    }
  ]
}
```

### 3. get_campaigns

Retrieves campaigns for a specific advertiser with optional filtering.

**Parameters:**
- `advertiser_id` (required): TikTok advertiser ID
- `filters` (optional): Filtering options
  - `campaign_ids`: List of campaign IDs to filter by (sent in TikTok's `filtering` object)
  - `campaign_name`: Fuzzy campaign-name filter
  - `primary_status`: Primary status filter
  - `secondary_status`: Secondary status filter
  - `objective_type`: Advertising objective filter
  - `campaign_automation_type`: `MANUAL`, `SMART_PLUS`, or `UPGRADED_SMART_PLUS`
  - `is_smart_performance_campaign`: Whether to return automated campaigns
  - `creation_filter_start_time` / `creation_filter_end_time`: Creation-time range
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Page size 1-1000 (default: 10)

**Example:**
```json
  "advertiser_id": "7441431575776520000",
  "filters": {
    "campaign_ids": ["123456789", "987654321"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "advertiser_id": "7441431575776520000",
  "count": 2,
  "page_info": {
    "page": 1,
    "page_size": 10,
    "total_page": 1,
    "total_number": 2
  },
  "campaigns": [
    {
      "campaign_id": "123456789",
      "campaign_name": "Summer Sale Campaign",
      "objective": "LANDING_PAGE",
      "budget": 1000.0,
      "budget_mode": "BUDGET_MODE_TOTAL",
      "operation_status": "ENABLE",
      "secondary_status": "CAMPAIGN_STATUS_ENABLE"
    }
  ]
}
```

### 4. get_ad_groups

Retrieves ad groups for a specific advertiser with comprehensive filtering.

**Parameters:**
- `advertiser_id` (required): TikTok advertiser ID
- `campaign_id` (optional): Campaign ID to filter by
- `filters` (optional): Advanced filtering options
  - `campaign_ids`: List of campaign IDs
  - `adgroup_ids`: List of ad group IDs
  - `adgroup_name`: Ad group name filter
  - `primary_status`: Primary status filter
  - `secondary_status`: Secondary status filter
  - `objective_type`: Advertising objective filter
  - `optimization_goal`: Optimization goal filter
  - `promotion_type`: Promotion type filter
  - `bid_strategy`: Bidding strategy filter
  - `creative_material_mode`: Creative material mode filter
  - `creation_filter_start_time`: Creation start time filter
  - `creation_filter_end_time`: Creation end time filter
  - `split_test_enabled`: Split test enabled filter
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Page size 1-1000 (default: 10)

**Example:**
```json
{
  "advertiser_id": "7441431575776520000",
  "campaign_id": "123456789",
  "filters": {
    "primary_status": "STATUS_ALL",
    "optimization_goal": "CLICK"
  },
  "page": 1,
  "page_size": 10
}
```

**Response:**
```json
{
  "success": true,
  "advertiser_id": "7441431575776520000",
  "campaign_id": "123456789",
  "count": 3,
  "ad_groups": [
    {
      "adgroup_id": "987654321",
      "adgroup_name": "Mobile Users",
      "campaign_id": "123456789",
      "budget": 500.0,
      "optimization_goal": "CLICK",
      "billing_event": "CPC",
      "operation_status": "ENABLE"
    }
  ]
}
```

### 5. get_ads

Retrieves ads for a specific advertiser with detailed filtering options.

**Parameters:**
- `advertiser_id` (required): TikTok advertiser ID
- `adgroup_id` (optional): Ad group ID to filter by
- `filters` (optional): Advanced filtering options
  - `campaign_ids`: List of campaign IDs
  - `adgroup_ids`: List of ad group IDs
  - `ad_ids`: List of ad IDs
  - `primary_status`: Primary status filter
  - `secondary_status`: Secondary status filter
  - `objective_type`: Advertising objective filter
  - `buying_types`: Buying types filter
  - `optimization_goal`: Optimization goal filter
  - `creative_material_mode`: Creative material mode filter
  - `destination`: Destination page type filter
  - `creation_filter_start_time`: Creation start time filter
  - `creation_filter_end_time`: Creation end time filter
  - `modified_after`: Modification time filter
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Page size 1-1000 (default: 10)

**Example:**
```json
{
  "advertiser_id": "7441431575776520000",
  "adgroup_id": "987654321",
  "filters": {
    "primary_status": "STATUS_ALL",
    "ad_format": "SINGLE_VIDEO"
  },
  "page": 1,
  "page_size": 10
}
```

**Response:**
```json
{
  "success": true,
  "advertiser_id": "7441431575776520000",
  "adgroup_id": "987654321",
  "count": 5,
  "ads": [
    {
      "ad_id": "555666777",
      "ad_name": "Summer Sale Video Ad",
      "adgroup_id": "987654321",
      "campaign_id": "123456789",
      "ad_format": "SINGLE_VIDEO",
      "operation_status": "ENABLE",
      "secondary_status": "AD_STATUS_ENABLE",
      "video_id": "video_123456",
      "landing_page_url": "https://example.com/sale"
    }
  ]
}
```

### 6. get_reports

Generates comprehensive performance reports and analytics.

**Parameters:**
- `advertiser_id` (conditional): TikTok advertiser ID (required for non-BC reports)
- `advertiser_ids` (conditional): List of advertiser IDs (max 5, for multi-advertiser reports)
- `bc_id` (conditional): Business Center ID (required for BC reports)
- `report_type` (required): Report type
  - `BASIC`: Basic performance reports
  - `AUDIENCE`: Audience insights reports
  - `PLAYABLE_MATERIAL`: Playable ads reports
  - `CATALOG`: DSA reports
  - `BC`: Business Center reports
  - `TT_SHOP`: Deprecated by TikTok; use the dedicated GMV Max report endpoint instead
- `data_level` (conditional): Data aggregation level
  - `AUCTION_AD`: Ad level
  - `AUCTION_ADGROUP`: Ad group level
  - `AUCTION_CAMPAIGN`: Campaign level
  - `AUCTION_ADVERTISER`: Advertiser level
- `dimensions` (required): Grouping conditions
- `metrics` (optional): Metrics to query
- `start_date` (conditional): Query start date (YYYY-MM-DD)
- `end_date` (conditional): Query end date (YYYY-MM-DD)
- `filters` (optional): Filtering conditions
- `service_type` (optional): Ad service type (AUCTION/RESERVATION)
- `query_lifetime` (optional): Request lifetime metrics
- `enable_total_metrics` (optional): Enable total metrics aggregation
- `multi_adv_report_in_utc_time` (optional): Use UTC timezone for multi-advertiser reports
- `order_field` (optional): Sorting field
- `order_type` (optional): Sorting order (ASC/DESC)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Page size 1-1000 (default: 10)

**Example:**
```json
{
  "advertiser_id": "7441431575776520000",
  "report_type": "BASIC",
  "data_level": "AUCTION_CAMPAIGN",
  "dimensions": ["campaign_id", "stat_time_day"],
  "metrics": ["spend", "impressions", "clicks", "ctr"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "filters": [
    {
      "field_name": "campaign_status",
      "filter_type": "IN",
      "filter_value": "[\"STATUS_ENABLE\"]"
    }
  ],
  "page": 1,
  "page_size": 10
}
```

**Response:**
```json
{
  "success": true,
  "report_type": "BASIC",
  "data_level": "AUCTION_CAMPAIGN",
  "total_metrics": {
    "spend": "1500.50",
    "impressions": "50000",
    "clicks": "750",
    "ctr": "1.5"
  },
  "page_info": {
    "page": 1,
    "page_size": 10,
    "total_number": 15,
    "total_page": 2
  },
  "count": 10,
  "reports": [
    {
      "dimensions": {
        "campaign_id": "123456789",
        "stat_time_day": "2024-01-15 00:00:00"
      },
      "metrics": {
        "spend": "100.25",
        "impressions": "3500",
        "clicks": "52",
        "ctr": "1.49"
      }
    }
  ]
}
```

## Examples

### Basic Workflow

1. **Get authorized accounts:**
```json
{"random_string": "test"}
```

2. **Get campaigns:**
```json
{
  "advertiser_id": "7441431575776520000",
  "page": 1,
  "page_size": 10
}
```

3. **Get ad groups for a campaign:**
```json
{
  "advertiser_id": "7441431575776520000",
  "campaign_id": "123456789",
  "page": 1,
  "page_size": 10
}
```

4. **Get ads for an ad group:**
```json
{
  "advertiser_id": "7441431575776520000",
  "adgroup_id": "987654321",
  "page": 1,
  "page_size": 10
}
```

5. **Generate performance report:**
```json
{
  "advertiser_id": "7441431575776520000",
  "report_type": "BASIC",
  "data_level": "AUCTION_CAMPAIGN",
  "dimensions": ["campaign_id", "stat_time_day"],
  "metrics": ["spend", "impressions", "clicks"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

### Advanced Filtering Examples

**Filter campaigns by status:**
```json
{
  "advertiser_id": "7441431575776520000",
  "filters": {
    "primary_status": "STATUS_ALL"
  }
}
```

**Filter ads by format and creation time:**
```json
{
  "advertiser_id": "7441431575776520000",
  "filters": {
    "ad_format": "SINGLE_VIDEO",
    "creation_filter_start_time": "2024-01-01 00:00:00",
    "creation_filter_end_time": "2024-01-31 23:59:59"
  }
}
```

**Multi-advertiser report:**
```json
{
  "advertiser_ids": ["123456789", "987654321"],
  "report_type": "BASIC",
  "data_level": "AUCTION_CAMPAIGN",
  "dimensions": ["advertiser_id", "stat_time_day"],
  "metrics": ["spend", "impressions"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "enable_total_metrics": true
}
```

## Error Handling

The MCP server provides comprehensive error handling:

### Common Error Types

1. **Authentication Errors:**
   - Missing or invalid credentials
   - Expired access tokens
   - Insufficient permissions

2. **Parameter Validation Errors:**
   - Missing required parameters
   - Invalid parameter values
   - Parameter type mismatches

3. **API Errors:**
   - Rate limiting
   - Invalid API calls
   - Server errors

### Error Response Format

```json
{
  "error": true,
  "message": "Error description",
  "suggestion": "Suggested action to resolve the error"
}
```

### Common Error Messages

- `"Missing required credentials"` - Check your environment variables
- `"Invalid access token"` - Refresh your access token
- `"Rate limit exceeded"` - Wait and retry the request
- `"Parameter validation failed"` - Check parameter values and types

## Best Practices

### 1. Authentication
- Keep your credentials secure
- Use environment variables for sensitive data
- Regularly rotate access tokens

### 2. Rate Limiting
- Implement exponential backoff for retries
- Monitor API usage limits
- Use pagination for large datasets

### 3. Data Management
- Use appropriate page sizes (10-100 for most queries)
- Implement proper error handling
- Cache frequently accessed data

### 4. Reporting
- Use appropriate date ranges (max 30 days for daily data)
- Enable total metrics for aggregated views
- Use filters to reduce data volume

> [!WARNING]
> `TT_SHOP` is rejected by this server because TikTok has marked the legacy GMV Max report as deprecated for the next API version. Migrate GMV Max reporting to `/gmv_max/report/get/` rather than relying on the legacy integrated report.

### 5. Performance
- Use specific filters to reduce response size
- Implement proper pagination
- Cache business center and advertiser data

### 6. Development
- Test with sandbox environment first
- Validate all parameters before API calls
- Implement comprehensive logging

## Troubleshooting

### Common Issues

1. **"0 tools enabled"**
   - Check MCP configuration in `~/.cursor/mcp.json`
   - Verify Python path and working directory
   - Restart Cursor after configuration changes

2. **Authentication failures**
   - Verify environment variables are set correctly
   - Check access token validity
   - Ensure proper permissions

3. **API errors**
   - Check parameter values and types
   - Verify date formats (YYYY-MM-DD)
   - Ensure required parameters are provided

4. **Performance issues**
   - Reduce page size
   - Use more specific filters
   - Implement caching where appropriate

### Getting Help

1. Check the logs in the `logs/` directory
2. Verify your configuration with `get_auth_info`
3. Test individual tools with minimal parameters
4. Review the TikTok Business API documentation

## Support

For issues and questions:
1. Check the project documentation
2. Review the TikTok Business API documentation
3. Open an issue on the GitHub repository
4. Contact the development team

---

*Last updated: November 26, 2025*
