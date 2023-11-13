import pytest

from wake import pars


class TestTokenizer:
    @pytest.mark.parametrize(
        "string, expected",
        [
            ("    5     ", dict(type="NUMBER", value="5")),
            ("55 # comment", dict(type="NUMBER", value="55")),
            (" # comment  ", dict(type=pars.EOF, value="")),
            ("      ", dict(type=pars.EOF, value="")),
            ("  'string' # comment", dict(type="STRING", value="'string'")),
        ],
    )
    def test_get_next(self, string, expected):
        tokenizer = pars.Tokenizer()
        tokenizer.string = string
        actual = tokenizer.get_next()
        assert actual.type == expected["type"]
        assert actual.value == expected["value"]
