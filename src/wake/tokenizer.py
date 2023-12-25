import collections
import re

Pattern = collections.namedtuple("Pattern", ["regexp", "name"])
Token = collections.namedtuple("Token", ["type", "value"], defaults=["", ""])

EOF = "EOF"
EOF_TOKEN = Token(type=EOF, value="")

NUMBER = r"\d+"
STRING = r"([\"'])(?:(?=(\\?))\2.)*?\1"
COMMENT = r"#.*$"
NEWLINE = r"\n"
NON_WS = r"\S*"
WS = r"[^\S\r\n]*"
IDENTIFIER = r"(?:[a-zA-Z]|_+[a-zA-Z0-9])+[a-zA-Z0-9_]*"

spec: list[Pattern] = [
    Pattern(WS, "WS"),
    Pattern(COMMENT, "COMMENT"),
    Pattern(NUMBER, "NUMBER"),
    Pattern(STRING, "STRING"),
    # Pattern(NON_WS, "NON_WS"),
    Pattern(IDENTIFIER, "IDENTIFIER"),
    Pattern(NEWLINE, "NEWLINE"),
]


class Tokenizer:
    def __init__(self) -> None:
        self.string = ""
        self.cursor = 0

    def get_next(self) -> Token:
        """Gets the next token in the input string.

        Returns:
            Token: The next token or EOF_TOKEN
                if there are no more tokens.

        Raises:
            SyntaxError: Unexpected token.
        """
        if not self.has_more_tokens():
            return EOF_TOKEN

        string = self.string[self.cursor :]
        for regexp, token_type in spec:
            value = self._match(r"^" + regexp, string)
            if not value:
                continue

            if token_type == "WS":
                return self.get_next()

            if token_type == "COMMENT":
                return self.get_next()

            return Token(
                type=token_type,
                value=value,
            )

        raise SyntaxError(f"Unexpected token: '{string[0]}'.")

    def _match(self, pattern: str, string: str) -> str | None:
        match = re.match(pattern, string, flags=re.IGNORECASE)
        if match:
            self.cursor += len(match[0])
            return match[0]
        return None

    def has_more_tokens(self) -> bool:
        """Checks if there are more tokens in the input string.

        Returns:
            bool: True if cursor is not at the end of the input,
                False otherwise.
        """
        return self.cursor < len(self.string)
