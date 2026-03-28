# SPEC.md — mcp-oeis

## Purpose

An MCP (Model Context Protocol) server that exposes the OEIS (Online Encyclopedia of Integer Sequences) API, allowing LLMs and applications to search and retrieve integer sequences.

## Scope

- **In scope:**
  - Search sequences by ID (e.g., A000109)
  - Search sequences by terms (e.g., 1,1,2,3,5,8)
  - Search sequences by name/keyword
  - Return parsed sequence data including name, description, and terms
- **Not in scope:**
  - User authentication with OEIS
  - Submitting new sequences
  - Binary data handling

## Public API / Interface

### MCP Tools

1. **`search_by_id`** - Get a sequence by its OEIS ID
   - Args: `id: str` (e.g., "A000109")
   - Returns: `dict` with sequence data

2. **`search_by_terms`** - Search sequences by integer terms
   - Args: `terms: list[int]` (e.g., [1,1,2,3,5,8])
   - Returns: `list[dict]` of matching sequences

3. **`search_by_name`** - Search sequences by name/keyword
   - Args: `query: str` (e.g., "Fibonacci")
   - Returns: `list[dict]` of matching sequences

### Data Structures

```python
SequenceData = {
    "id": str,           # e.g., "A000045"
    "name": str,         # e.g., "Fibonacci numbers"
    "terms": list[int],  # e.g., [0,1,1,2,3,5,8,13,...]
    "description": str,  # Full description from OEIS
    "offset": int,       # Index offset (usually 0 or 1)
    "comments": str,     # Additional comments
    "references": str,   # References to literature
    "links": str,        # Related links
    " formula": str,     # Formula if available
    "example": str,      # Example terms
}
```

## Edge Cases

1. **Invalid ID format** - Should raise ValueError for non-Axxxxxx format
2. **No results found** - Return empty list with informative message
3. **Network failure** - Raise appropriate exception with retry suggestion
4. **Malformed response** - Handle gracefully with error message
5. **Empty search terms** - Raise ValueError
6. **Rate limiting** - Add delay between requests (OEIS requests polite behavior)
7. **Very long sequences** - Truncate display but include full data

## Performance & Constraints

- Use `fmt=text` for simpler parsing
- Add 1 second delay between requests to respect OEIS usage policy
- Cache recent queries to reduce redundant requests
- Timeout after 30 seconds for any single request

## MCP Configuration

- Transport: stdio
- Package: fastmcp
