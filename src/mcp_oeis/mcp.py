from typing import Any

import fastmcp

from mcp_oeis.client import OEISClient

mcp = fastmcp.FastMCP("mcp-oeis")


@mcp.tool()
def get_sequence_by_id(id: str) -> dict[str, Any]:
    """Get a sequence by its OEIS ID (e.g., "A000109" for simplicial polyhedra, "A000045" for Fibonacci).

    Args:
        id: The OEIS ID (e.g., "A000109", "A000045")

    Returns:
        Dictionary containing:
            - id: The OEIS ID
            - name: Sequence name/description
            - terms: List of integers in the sequence
            - offset: Index offset (where sequence starts)
            - description: Full description
            - comments: Additional comments
            - references: Literature references
            - links: Related links
            - formula: Formula if available
            - example: Example terms

    Raises:
        ValueError: If the ID format is invalid or sequence not found
    """
    client = OEISClient()
    try:
        seq = client.get_sequence_by_id(id)
        return {
            "id": seq.id,
            "name": seq.name,
            "terms": seq.terms,
            "offset": seq.offset,
            "description": seq.description,
            "comments": seq.comments,
            "references": seq.references,
            "links": seq.links,
            "formula": seq.formula,
            "example": seq.example,
        }
    finally:
        client.close()


@mcp.tool()
def search_by_terms(terms: list[int], max_results: int = 10) -> list[dict[str, Any]]:
    """Search OEIS sequences by providing integer terms.

    For example, searching [1,1,2,3,5,8] will find the Fibonacci sequence.

    Args:
        terms: List of integers to search for (e.g., [1,1,2,3,5,8])
        max_results: Maximum number of results to return (default 10)

    Returns:
        List of matching sequences, each containing:
            - id: The OEIS ID
            - name: Sequence name
            - terms: First few terms of the sequence

    Raises:
        ValueError: If terms list is empty
    """
    client = OEISClient()
    try:
        results = client.search_by_terms(terms, max_results)
        return [
            {
                "id": r.id,
                "name": r.name,
                "terms": r.terms,
            }
            for r in results
        ]
    finally:
        client.close()


@mcp.tool()
def search_by_name(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Search OEIS sequences by name or keyword.

    For example, searching "Fibonacci" will find Fibonacci-related sequences.

    Args:
        query: Search query (e.g., "Fibonacci", "prime", "Catalan")
        max_results: Maximum number of results to return (default 10)

    Returns:
        List of matching sequences, each containing:
            - id: The OEIS ID
            - name: Sequence name
            - terms: First few terms of the sequence

    Raises:
        ValueError: If query is empty
    """
    client = OEISClient()
    try:
        results = client.search_by_name(query, max_results)
        return [
            {
                "id": r.id,
                "name": r.name,
                "terms": r.terms,
            }
            for r in results
        ]
    finally:
        client.close()
