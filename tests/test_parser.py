import pytest

from wake import pars


@pytest.fixture
def parser() -> pars.Parser:
    return pars.Parser()


@pytest.mark.parametrize(
    "string, expected",
    [
        ("   'one'", "one"),
        ('"two"    ', "two"),
        ('   "two"    ', "two"),
    ],
)
def test_ignore_whitespace(parser, string: pars.Parser, expected):
    actual = parser.parse(string)
    literal = dict(type="literal", value=dict(type="string", value=expected))
    assert actual == literal


class TestLiteral:
    @pytest.mark.parametrize(
        "string, expected",
        [
            ("5", 5),
            ("55", 55),
            ("355", 355),
        ],
    )
    def test_number(self, parser, string, expected):
        actual = parser.parse(string)
        literal = dict(type="literal", value=dict(type="number", value=expected))
        assert actual == literal

    @pytest.mark.parametrize(
        "string, expected",
        [
            ("'one'", "one"),
            ('"two"', "two"),
        ],
    )
    def test_string(self, parser, string, expected):
        actual = parser.parse(string)
        literal = dict(type="literal", value=dict(type="string", value=expected))
        assert actual == literal

    @pytest.mark.parametrize(
        "string, expected",
        [
            ("'one'", dict(type="string", value="one")),
            ('"two"', dict(type="string", value="two")),
            ("55", dict(type="number", value=55)),
        ],
    )
    def test_literal(self, parser, string, expected):
        actual = parser.parse(string)
        literal = dict(type="literal", value=expected)
        assert actual == literal


class TestVariable:
    @pytest.mark.parametrize(
        "string, expected",
        [
            ('VAR="foo"', ""),
            ("VAR=foo", ""),
            ("VAR=foo_bar", ""),
            ("VAR=foo-bar", ""),
            ("VAR=_foo", ""),
            ("VAR=foo", ""),
        ],
    )
    def test_variable_ok(self, parser, string, expected):
        actual = parser.parse(string)
        variable = dict(type="variable", value=dict(type="string", value=expected))
        assert actual == variable

    @pytest.mark.parametrize(
        "string, expected",
        [
            ("aVaR", None)
            ("_var_", None)
            ("V_a__r", None)
            ("VAR", None)
            ("var", None)
            ("___VAr___", None)
        ],
    )
    def test_variable_ok(self, parser, string, expected):
        actual = parser.parse(string)
        variable = dict(type="variable", value=dict(type="string", value=expected))
        assert actual == variable


    @pytest.mark.parametrize(
        "string, expected_err",
        [
            ('VAR=="foo"', SyntaxError),
            ("VAR=fo-_o", SyntaxError),
            ("VAR=foo_bar", SyntaxError),
            ("VAR=foo-bar", SyntaxError),
            ("VAR=_foo", SyntaxError),
            ("VAR=foo", SyntaxError),
        ],
    )
    def test_variable_fail(self, parser, string, expected_err):
        with pytest.raises(ValueError):
            _ = parser.parse(string)
