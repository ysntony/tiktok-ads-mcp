"""Shared helpers for preserving TikTok responses and pagination metadata."""

from typing import Any


def as_float(value: Any, default: float = 0.0) -> float:
    """Convert numeric API fields without failing an otherwise valid response."""
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def preserve_item(item: dict[str, Any]) -> dict[str, Any]:
    """Return a shallow copy so new API fields are not silently discarded."""
    return dict(item)


def with_metadata(items: list[dict[str, Any]], data: dict[str, Any], include_metadata: bool) -> Any:
    """Keep the historical list return by default, with opt-in pagination metadata."""
    if not include_metadata:
        return items
    return {
        "list": items,
        "page_info": data.get("page_info", {}),
    }
