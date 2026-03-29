from collections.abc import Callable
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_oeis_response() -> Callable[[str], MagicMock]:
    def _mock_response(data: str) -> MagicMock:
        mock = MagicMock()
        mock.text = data
        mock.raise_for_status = MagicMock()
        return mock

    return _mock_response


@pytest.fixture
def sample_sequence_data() -> str:
    return """# Greetings from The On-Line Encyclopedia of Integer Sequences! http://oeis.org/
Search: id:a000109
Showing 1-1 of 1
%I A000109 M1469 N0580
%S A000109 1,1,1,2,5,14,50,233,1249,7595,49566,339722
%N A000109 Number of simplicial polyhedra with n vertices.
%C A000109 This is a comment about the sequence.
%F A000109 a(n) = some formula here.
%O A000109 3
"""


@pytest.fixture
def sample_search_results() -> str:
    return """# Greetings from The On-Line Encyclopedia of Integer Sequences! http://oeis.org/
Search: Fibonacci
Showing 1-2 of 2
%I A000045 M0692 N0256
%S A000045 0,1,1,2,3,5,8,13,21,34
%N A000045 Fibonacci numbers: F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1.
%I A001353 M0780 N0299
%S A001353 0,1,3,8,21,55,144
%N A001353 F(2n) = bisection of Fibonacci sequence: a(n) = 3*a(n-1) - a(n-2).
"""
