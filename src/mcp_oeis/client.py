import re
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import httpx

OEIS_BASE_URL = "https://oeis.org"


@dataclass
class SequenceData:
    id: str
    name: str
    terms: list[int]
    offset: int = 0
    description: str = ""
    comments: str = ""
    references: str = ""
    links: str = ""
    formula: str = ""
    example: str = ""


@dataclass
class SearchResult:
    id: str
    name: str
    terms: str


class OEISClient:
    def __init__(self, timeout: float = 30.0, delay: float = 1.0) -> None:
        self._client = httpx.Client(timeout=timeout)
        self._delay = delay
        self._last_request_time = 0.0

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_time
        if elapsed < self._delay:
            time.sleep(self._delay - elapsed)
        self._last_request_time = time.time()

    def _validate_id(self, id: str) -> None:
        if not re.match(r"^A\d{6}$", id.upper()):
            raise ValueError(f"Invalid OEIS ID format: {id}. Expected format: A000000")

    def get_sequence_by_id(self, id: str) -> SequenceData:
        self._validate_id(id)
        self._rate_limit()

        url = f"{OEIS_BASE_URL}/search?fmt=text&q=id:{id}"
        response = self._client.get(url)
        response.raise_for_status()

        return self._parse_sequence_response(response.text, id.upper())

    def search_by_name(self, query: str, max_results: int = 10) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Search query cannot be empty")

        self._rate_limit()
        url = f"{OEIS_BASE_URL}/search"
        params = {"fmt": "text", "q": query, "max": str(max_results)}
        response = self._client.get(url, params=params)
        response.raise_for_status()

        return self._parse_search_results(response.text)

    def search_by_terms(
        self, terms: list[int], max_results: int = 10
    ) -> list[SearchResult]:
        if not terms:
            raise ValueError("Search terms cannot be empty")

        self._rate_limit()
        terms_str = ",".join(str(t) for t in terms)
        url = f"{OEIS_BASE_URL}/search"
        params = {"fmt": "text", "q": terms_str, "max": str(max_results)}
        response = self._client.get(url, params=params)
        response.raise_for_status()

        return self._parse_search_results(response.text)

    def _parse_sequence_response(self, text: str, target_id: str) -> SequenceData:
        lines = text.strip().split("\n")

        if not lines or "Showing 0-" in lines[0]:
            raise ValueError(f"Sequence not found: {target_id}")

        data: dict[str, Any] = {
            "id": target_id,
            "name": "",
            "terms": [],
            "offset": 0,
            "description": "",
            "comments": "",
            "references": "",
            "links": "",
            "formula": "",
            "example": "",
        }

        terms_lines: list[str] = []
        for line in lines:
            if not line:
                continue
            code = line[:2]
            content = line[2:].strip()

            if code == "%N":
                name_content = content
                if name_content.startswith(target_id):
                    name_content = name_content[len(target_id) :].strip()
                data["name"] = name_content
            elif code == "%S":
                terms_lines.append(content)
            elif code == "%T":
                terms_lines.append(content)
            elif code == "%U":
                terms_lines.append(content)
            elif code == "%C":
                data["comments"] += content + "\n"
            elif code == "%R":
                data["references"] += content + "\n"
            elif code == "%H":
                data["links"] += content + "\n"
            elif code == "%F":
                data["formula"] += content + "\n"
            elif code == "%E":
                data["example"] += content + "\n"
            elif code == "%O":
                try:
                    data["offset"] = int(content.split(",")[0].strip())
                except ValueError:
                    pass
            elif code == "%D":
                data["description"] += content + "\n"

        all_terms = "".join(terms_lines)
        terms_match = re.findall(r"-?\d+", all_terms)
        data["terms"] = [int(t) for t in terms_match]

        return SequenceData(
            id=data["id"],
            name=data["name"],
            terms=data["terms"],
            offset=data["offset"],
            description=data["description"].strip(),
            comments=data["comments"].strip(),
            references=data["references"].strip(),
            links=data["links"].strip(),
            formula=data["formula"].strip(),
            example=data["example"].strip(),
        )

    def _parse_search_results(self, text: str) -> list[SearchResult]:
        lines = text.strip().split("\n")

        if not lines:
            return []

        results: list[SearchResult] = []
        for line in lines:
            if not line or line.startswith("#"):
                continue
            if "Showing 0-" in line:
                continue

            id_match = re.match(r"^(\w)\s*(\w)(\d+)\s*(.+)$", line)
            if id_match:
                seq_num = id_match.group(3)
                seq_id = f"A{seq_num}"
                seq_name = id_match.group(4).strip()
                results.append(SearchResult(id=seq_id, name=seq_name, terms=""))

        return results

    def close(self) -> None:
        self._client.close()


@lru_cache(maxsize=128)
def _cached_search_by_name(
    query: str, max_results: int
) -> tuple[str, list[dict[str, Any]]]:
    client = OEISClient()
    try:
        results = client.search_by_name(query, max_results)
        return query, [{"id": r.id, "name": r.name, "terms": r.terms} for r in results]
    finally:
        client.close()
