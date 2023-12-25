import json

import pytest

from wake.parser import Parser


@pytest.mark.parametrize(
    "parser, expected",
    [
        (
            'VAR="foo"',
            """
{
    "type": "VariableDeclaration",
    "kind": "var",
    "declarations": [
        {
            "type": "VariableDeclarator",
            "id": {
                "type": "Identifier",
                "name": "VAR"
            },
            "init": {
                "type": "Literal",
                "value": "foo",
                "raw": "'foo'"
            }
        }
    ]
}
""",
        ),
        (
            "VAR=1",
            """
{
    "type": "VariableDeclaration",
    "kind": "var",
    "declarations": [
        {
            "type": "VariableDeclarator",
            "id": {
               "type": "Identifier",
                "name": "VAR"
            },
            "init": {
                "type": "Literal",
                "value": 1,
                "raw": "'1'"
            }
        }
    ]
}
    """,
        ),
        # ("VAR=foo_bar", ""),
        # ("VAR=_foo", ""),
        # ("VAR=foo", ""),
    ],
    indirect=["parser"],
)
def test_variable_declaration_nominal(parser: Parser, expected):
    # parser.string = string
    # parser.lookahead = parser.tokenizer.get_next()
    actual = parser.variable_declaration()
    x = json.loads(expected)
    print(x)
    assert actual == x
