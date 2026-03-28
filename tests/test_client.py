from unittest.mock import MagicMock, patch

import pytest

from mcp_oeis.client import OEISClient, SequenceData


class TestOEISClient:
    def test_validate_id_valid(self) -> None:
        client = OEISClient()
        client._validate_id("A000109")
        client._validate_id("a000109")
        client.close()

    def test_validate_id_invalid(self) -> None:
        client = OEISClient()
        with pytest.raises(ValueError, match="Invalid OEIS ID format"):
            client._validate_id("invalid")
        with pytest.raises(ValueError, match="Invalid OEIS ID format"):
            client._validate_id("B000109")
        with pytest.raises(ValueError, match="Invalid OEIS ID format"):
            client._validate_id("A00010")
        client.close()

    @patch("mcp_oeis.client.httpx.Client")
    def test_get_sequence_by_id(
        self,
        mock_client_class: MagicMock,
        sample_sequence_data: str,
    ) -> None:
        mock_response = MagicMock()
        mock_response.text = sample_sequence_data
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = OEISClient()
        result = client.get_sequence_by_id("A000109")

        assert result.id == "A000109"
        assert result.name == "Number of simplicial polyhedra with n vertices."
        assert 1 in result.terms
        assert 2 in result.terms
        client.close()

    @patch("mcp_oeis.client.httpx.Client")
    def test_search_by_terms(
        self,
        mock_client_class: MagicMock,
        sample_search_results: str,
    ) -> None:
        mock_response = MagicMock()
        mock_response.text = sample_search_results
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = OEISClient()
        result = client.search_by_terms([0, 1, 1, 2, 3, 5])

        assert len(result) >= 1
        assert result[0].id == "A000045"
        client.close()

    @patch("mcp_oeis.client.httpx.Client")
    def test_search_by_name(
        self,
        mock_client_class: MagicMock,
        sample_search_results: str,
    ) -> None:
        mock_response = MagicMock()
        mock_response.text = sample_search_results
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = OEISClient()
        result = client.search_by_name("Fibonacci")

        assert len(result) >= 1
        assert result[0].id == "A000045"
        client.close()

    def test_search_by_name_empty_query(self) -> None:
        client = OEISClient()
        with pytest.raises(ValueError, match="Search query cannot be empty"):
            client.search_by_name("")
        client.close()

    def test_search_by_terms_empty_terms(self) -> None:
        client = OEISClient()
        with pytest.raises(ValueError, match="Search terms cannot be empty"):
            client.search_by_terms([])
        client.close()

    @patch("mcp_oeis.client.httpx.Client")
    def test_get_sequence_not_found(self, mock_client_class: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.text = "Showing 0-0 of 0"
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = OEISClient()
        with pytest.raises(ValueError, match="Sequence not found"):
            client.get_sequence_by_id("A999999")
        client.close()

    @patch("mcp_oeis.client.httpx.Client")
    def test_parse_sequence_response_with_offset(
        self, mock_client_class: MagicMock
    ) -> None:
        response_text = """%I A000045
%S A000045 0,1,1,2,3,5,8,13
%O A000045 0
"""
        mock_response = MagicMock()
        mock_response.text = response_text
        mock_response.raise_for_status = MagicMock()

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = OEISClient()
        result = client.get_sequence_by_id("A000045")

        assert result.offset == 0
        assert 0 in result.terms
        client.close()


class TestSequenceData:
    def test_sequence_data_creation(self) -> None:
        seq = SequenceData(
            id="A000045",
            name="Fibonacci numbers",
            terms=[0, 1, 1, 2, 3, 5],
            offset=0,
            description="The Fibonacci sequence",
        )
        assert seq.id == "A000045"
        assert seq.name == "Fibonacci numbers"
        assert seq.terms == [0, 1, 1, 2, 3, 5]
        assert seq.offset == 0
