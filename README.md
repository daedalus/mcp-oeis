# mcp-oeis

> MCP server for the OEIS (Online Encyclopedia of Integer Sequences) API

mcp-name: io.github.daedalus/mcp-oeis

[![PyPI](https://img.shields.io/pypi/v/mcp-oeis.svg)](https://pypi.org/project/mcp-oeis/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-oeis.svg)](https://pypi.org/project/mcp-oeis/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install mcp-oeis
```

## Usage

### As an MCP Server

Configure in your MCP settings:

```json
{
  "mcpServers": {
    "mcp-oeis": {
      "command": "mcp-oeis"
    }
  }
}
```

### Python API

```python
from mcp_oeis import mcp

# Get a sequence by ID
result = mcp.get_sequence_by_id("A000109")
print(result["terms"])  # [1, 1, 1, 2, 5, 14, ...]

# Search by terms
results = mcp.search_by_terms([1, 1, 2, 3, 5, 8])
print(results[0]["name"])  # "Fibonacci numbers"

# Search by name
results = mcp.search_by_name("prime")
print(results[0]["id"])  # "A000040"
```

## MCP Tools

### get_sequence_by_id
Get a sequence by its OEIS ID (e.g., "A000109" for simplicial polyhedra, "A000045" for Fibonacci).

### search_by_terms
Search OEIS sequences by providing integer terms. For example, searching [1,1,2,3,5,8] will find the Fibonacci sequence.

### search_by_name
Search OEIS sequences by name or keyword. For example, searching "Fibonacci" will find Fibonacci-related sequences.

## Development

```bash
git clone https://github.com/daedalus/mcp-oeis.git
cd mcp-oeis
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```
