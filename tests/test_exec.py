import pytest

from wake.parser import Parser


@pytest.mark.parametrize(
    "parser, expected",
    [
        (
            f"VAR={raw}",
            {
                "type": "VariableDeclaration",
                "value": {
                    "type": "VariableDeclarator",
                    "id": {
                        "type": "Identifier",
                        "name": "VAR",
                    },
                    "init": {
                        "type": "Literal",
                        "value": value,
                        "raw": raw,
                    },
                },
            },
        )
        for value, raw in [("foo", '"foo"'), (1, "1")]
    ],
    indirect=["parser"],
)
def test_variable_declaration_literal(parser: Parser, expected):
    # parser.string = string
    # parser.lookahead = parser.tokenizer.get_next()
    actual = parser.variable_declaration()
    assert actual == expected
