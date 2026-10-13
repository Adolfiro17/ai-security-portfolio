"""
The three tools available to the Northwind Retail IT support agent.
"""
from __future__ import annotations

from typing import Callable

from app.data import ASSET_INVENTORY, TicketStore, read_support_doc


def read_support_docs(filename: str) -> str:
    """Read one support document by filename."""
    return read_support_doc(filename)


def make_create_ticket(store: TicketStore) -> Callable:
    """Bind create_ticket to a specific ticket store."""
    def create_ticket(subject: str, body: str, created_by: str = "unknown") -> dict:
        return store.create(subject=subject, body=body, created_by=created_by)
    return create_ticket


def query_asset_inventory(asset_id: str) -> dict:
    """Look up one asset record by ID. Returns restricted records too, so callers
    must not assume everything returned here is safe to show a user."""
    record = ASSET_INVENTORY.get(asset_id)
    if record is None:
        return {"error": f"No such asset: {asset_id}"}
    return record


# Tool registry. "high_impact" tools need human approval in the hardened agent,
# even when they are on the allow-list.
TOOL_SCHEMAS: dict[str, dict] = {
    "read_support_docs": {"description": "Read a support document by filename.", "high_impact": False},
    "create_ticket": {"description": "Create an IT support ticket.", "high_impact": False},
    "query_asset_inventory": {"description": "Look up an asset record by ID.", "high_impact": True},
}
