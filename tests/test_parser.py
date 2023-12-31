import pytest

from wake.parser import Parser


@pytest.fixture
def parser() -> Parser:
    return Parser()


# @pytest.mark.parametrize(
#     "string, expected",
#     [
#         ("   'one'", "one"),
#         ('"two"    ', "two"),
#         ('   "two"    ', "two"),
#     ],
# )
# def test_ignore_whitespace(parser, string: Parser, expected):
#     actual = parser.parse(string)
#     literal = {"type": "literal", "value": {"type": "string", "value": expected}}
#     assert actual == literal


# class TestLiteral:
#     @pytest.mark.parametrize(
#         "string, expected",
#         [
#             ("5", 5),
#             ("55", 55),
#             ("355", 355),
#         ],
#     )
#     def test_number(self, parser, string, expected):
#         actual = parser.parse(string)
#         literal = {"type": "literal", "value": {"type": "number", "value": expected}}
#         assert actual == literal

#     @pytest.mark.parametrize(
#         "string, expected",
#         [
#             ("'one'", "one"),
#             ('"two"', "two"),
#         ],
#     )
#     def test_string(self, parser, string, expected):
#         actual = parser.parse(string)
#         literal = {"type": "literal", "value": {"type": "string", "value": expected}}
#         assert actual == literal

#     @pytest.mark.parametrize(
#         "string, expected",
#         [
#             ("'one'", {"type": "string", "value": "one"}),
#             ('"two"', {"type": "string", "value": "two"}),
#             ("55", {"type": "number", "value": 55}),
#         ],
#     )
#     def test_literal(self, parser, string, expected):
#         actual = parser.parse(string)
#         literal = {"type": "literal", "value": expected}
#         assert actual == literal


# class TestVariable:
#     @pytest.mark.parametrize(
#         "string, expected",
#         [
#             ('VAR="foo"', ""),
#             ("VAR=foo", ""),
#             ("VAR=foo_bar", ""),
#             ("VAR=foo-bar", ""),
#             ("VAR=_foo", ""),
#             ("VAR=foo", ""),
#         ],
#     )
#     def test_variable_ok(self, parser, string, expected):
#         actual = parser.parse(string)
#         variable = {"type": "variable", "value": {"type": "string", "value": expected}}
#         assert actual == variable

#     @pytest.mark.parametrize(
#         "string, expected",
#         [
#             ("aVaR", None)("_var_", None)("V_a__r", None)("VAR", None)("var", None)(
#                 "___VAr___", None
#             )("_557", None)("v557", None)("v5_5_", None)
#         ],
#     )
#     def test_variable_ok_2(self, parser, string, expected):
#         actual = parser.string = string
#         variable = {"type": "variable", "value": {"type": "identifier", "value": expected}}
#         assert actual == variable

#     @pytest.mark.parametrize(
#         "string, expected_err",
#         [
#             ('VAR=="foo"', SyntaxError),
#             ("VAR=fo-_o", SyntaxError),
#             ("VAR=foo_bar", SyntaxError),
#             ("VAR=foo-bar", SyntaxError),
#             ("VAR=_foo", SyntaxError),
#             ("VAR=foo", SyntaxError),
#         ],
#     )
#     def test_variable_fail(self, parser, string, expected_err):
#         with pytest.raises(ValueError):
#             _ = parser.parse(string)
