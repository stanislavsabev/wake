import pytest

from wake import pars


@pytest.fixture
def new_parser() -> pars.Parser:
    return pars.Parser()


@pytest.fixture
def prep_parser(new_parser, request):
    string = request.param
    new_parser.string = string
    new_parser.tokenizer.string = string
    return new_parser


@pytest.mark.parametrize(
    "prep_parser, expected",
    [
        ("   'one'", "one"),
        ('"two"    ', "two"),
        ('   "two"    ', "two"),
    ],
    indirect=["prep_parser"],
)
def test_ignore_whitespace(prep_parser: pars.Parser, expected):
    parser = prep_parser
    parser.lookahead = parser.tokenizer.get_next()
    actual = prep_parser.string_lit()
    assert actual["type"] == "string"
    assert actual["value"] == expected


class TestLiteral:
    @pytest.mark.parametrize(
        "prep_parser, expected",
        [
            ("5", 5),
            ("55", 55),
            ("355", 355),
        ],
        indirect=["prep_parser"],
    )
    def test_number(self, prep_parser, expected):
        parser = prep_parser
        parser.lookahead = parser.tokenizer.get_next()
        actual = prep_parser.number_lit()
        assert actual["type"] == "number"
        assert actual["value"] == expected

    @pytest.mark.parametrize(
        "prep_parser, expected",
        [
            ("'one'", "one"),
            ('"two"', "two"),
        ],
        indirect=["prep_parser"],
    )
    def test_string(self, prep_parser, expected):
        parser = prep_parser
        parser.lookahead = parser.tokenizer.get_next()
        actual = prep_parser.string_lit()
        assert actual["type"] == "string"
        assert actual["value"] == expected

    @pytest.mark.parametrize(
        "prep_parser, expected",
        [
            ("'one'", dict(type="string", value="one")),
            ('"two"', dict(type="string", value="two")),
            ("55", dict(type="number", value=55)),
        ],
        indirect=["prep_parser"],
    )
    def test_literal(self, prep_parser, expected):
        parser = prep_parser
        parser.lookahead = parser.tokenizer.get_next()
        actual = prep_parser.literal()
        assert actual["type"] == "literal"
        assert actual["value"] == expected


class TestVariable:
    @pytest.mark.parametrize(
        "prep_parser, expected",
        [
            ('VAR="foo"', ""),
            ("VAR=foo", ""),
            ("VAR=foo_bar", ""),
            ("VAR=foo-bar", ""),
            ("VAR=_foo", ""),
            ("VAR=foo", ""),
        ],
        indirect=["prep_parser"],
    )
    def test_variable_ok(self, prep_parser, expected):
        parser = prep_parser
        parser.lookahead = parser.tokenizer.get_next()

        actual = prep_parser.string_lit()
        assert actual["type"] == "string"
        assert actual["value"] == expected

    @pytest.mark.parametrize(
        "string, expected",
        [
            ('VAR=="foo"', SyntaxError),
            ("VAR=fo-_o", SyntaxError),
            ("VAR=foo_bar", SyntaxError),
            ("VAR=foo-bar", SyntaxError),
            ("VAR=_foo", SyntaxError),
            ("VAR=foo", SyntaxError),
        ],
    )
    def test_variable_fail(self, new_parser, string, expected):
        parser = prep_parser
        parser.lookahead = parser.tokenizer.get_next()
        actual = parser.string_lit()

        assert actual["type"] == "string"
        assert actual["value"] == expected
