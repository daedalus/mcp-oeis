from unittest.mock import MagicMock, patch

from mcp_oeis.client import SearchResult, SequenceData
from mcp_oeis.mcp import get_sequence_by_id, search_by_name, search_by_terms


class TestMCP:
    @patch("mcp_oeis.mcp.OEISClient")
    def test_get_sequence_by_id(self, mock_client_class: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.get_sequence_by_id.return_value = SequenceData(
            id="A000109",
            name="Number of simplicial polyhedra",
            terms=[1, 1, 1, 2, 5, 14],
            offset=3,
            description="Test description",
        )
        mock_client_class.return_value = mock_client

        result = get_sequence_by_id("A000109")

        assert result["id"] == "A000109"
        assert result["name"] == "Number of simplicial polyhedra"
        assert 1 in result["terms"]
        assert 14 in result["terms"]
        mock_client.get_sequence_by_id.assert_called_once_with("A000109")
        mock_client.close.assert_called_once()

    @patch("mcp_oeis.mcp.OEISClient")
    def test_search_by_terms(self, mock_client_class: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.search_by_terms.return_value = [
            SearchResult(id="A000045", name="Fibonacci numbers", terms="0,1,1,2,3")
        ]
        mock_client_class.return_value = mock_client

        result = search_by_terms([0, 1, 1, 2, 3, 5])

        assert len(result) == 1
        assert result[0]["id"] == "A000045"
        assert result[0]["name"] == "Fibonacci numbers"
        mock_client.search_by_terms.assert_called_once()
        mock_client.close.assert_called_once()

    @patch("mcp_oeis.mcp.OEISClient")
    def test_search_by_name(self, mock_client_class: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.search_by_name.return_value = [
            SearchResult(id="A000045", name="Fibonacci numbers", terms="0,1")
        ]
        mock_client_class.return_value = mock_client

        result = search_by_name("Fibonacci")

        assert len(result) == 1
        assert result[0]["id"] == "A000045"
        mock_client.search_by_name.assert_called_once()
        mock_client.close.assert_called_once()

    @patch("mcp_oeis.mcp.OEISClient")
    def test_search_by_name_with_max_results(
        self, mock_client_class: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.search_by_name.return_value = []
        mock_client_class.return_value = mock_client

        search_by_name("test", max_results=5)

        mock_client.search_by_name.assert_called_once_with("test", 5)

    @patch("mcp_oeis.mcp.OEISClient")
    def test_get_sequence_returns_all_fields(
        self, mock_client_class: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.get_sequence_by_id.return_value = SequenceData(
            id="A000045",
            name="Fibonacci numbers",
            terms=[0, 1, 1],
            offset=0,
            description="The Fibonacci numbers",
            comments="Some comment",
            references="Reference here",
            links="http://example.com",
            formula="F(n) = F(n-1) + F(n-2)",
            example="Example here",
        )
        mock_client_class.return_value = mock_client

        result = get_sequence_by_id("A000045")

        assert "description" in result
        assert "comments" in result
        assert "references" in result
        assert "links" in result
        assert "formula" in result
        assert "example" in result
        assert result["formula"] == "F(n) = F(n-1) + F(n-2)"
