"""Test CLI entry point."""

import pytest

from wake.parser import Parser


@pytest.fixture
def parser(request) -> Parser:
    p = Parser()
    if hasattr(request, "param"):
        p.string = request.param
        p.tokenizer.string = request.param
        p.lookahead = p.tokenizer.get_next()
    yield p
