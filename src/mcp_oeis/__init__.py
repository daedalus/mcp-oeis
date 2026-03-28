__version__ = "0.1.0"
__all__ = ["client", "mcp"]

from typing import TYPE_CHECKING

from .mcp import mcp

if TYPE_CHECKING:
    from .client import OEISClient, SearchResult, SequenceData
