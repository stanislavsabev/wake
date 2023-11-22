import collections
import re

from wake.typedef import AnyDict


Pattern = collections.namedtuple("Pattern", ["regexp", "name"])
Token = collections.namedtuple("Token", ["type", "value"], defaults=["", ""])

EOF = "EOF"
EOF_TOKEN = Token(type=EOF, value="")

NUMBER = r"\d+"
STRING = r"([\"'])(?:(?=(\\?))\2.)*?\1"
COMMENT = r"#.*$"
NL = r"\n"
NON_WS = r"\S*"
WS = r"[^\S\r\n]*"
IDENTIFIER = r"[a-zA-Z_]+(?:(?:_(?!-)|-(?!_))|[a-zA-Z0-9])*[a-zA-Z0-9_]+"

spec: list[Pattern] = [
    Pattern(WS, "WS"),
    Pattern(COMMENT, "COMMENT"),
    Pattern(NUMBER, "NUMBER"),
    Pattern(STRING, "STRING"),
    # Pattern(NON_WS, "NON_WS"),
    Pattern(IDENTIFIER, "IDENTIFIER"),
    Pattern(NL, "NL"),
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


class Parser:
    def __init__(self) -> None:
        self.string = ""
        self.tokenizer = Tokenizer()
        self.lookahead = EOF_TOKEN

    def _consume(self, token_type: str) -> Token:
        """Consumes token of particular type.

        Args:
            token_type (str): Token type to consume.

        Raises:
            SyntaxError: Unexpected end of input, if there are no more tokens.
            SyntaxError: Unexpected token.

        Returns:
            Token: Consumed token.
        """
        token = self.lookahead
        if token.type == EOF:
            raise SyntaxError(f"Unexpected end of input, expected: '{token_type}'")

        if token.type != token_type:
            raise SyntaxError(
                "Unexpected token." f" Expected: '{token_type}', got '{token.type}'."
            )

        self.lookahead = self.tokenizer.get_next()
        return token

    def parse(self, string) -> Token:
        self.string = string
        self.tokenizer.string = string
        self.lookahead = self.tokenizer.get_next()
        return self.variables()

    def wakefile(self) -> AnyDict:
        # statement list
        value: dict[str, AnyDict] = {}

        if variables := self.variables():
            value.update(variables=variables)
        if procecures := self.procecures():
            value.update(procecures=procecures)

        return dict(type="wakefile", value=value)

    def variables(self) -> list[AnyDict]:
        variables = []
        while self.lookahead != "LABEL":
            statement = self.statement()
            variables.append(statement)
        return variables

    def procecures(self) -> list[AnyDict]:
        procecures = []
        return procecures

    def statement(self) -> AnyDict:
        if self.lookahead == "IDENTIFIER":
            return self.variable_statement()
        else:
            return self.literal()

    def variable_statement(self) -> AnyDict:
        name = self._consume("IDENTIFIER")
        self._consume("=")
        initializer = self.variable_initializer()
        variable_declaration = dict(
            type="variable_declaration",
            id=dict(
                type="identifier",
                name=name,
                init=initializer,
            ),
        )
        return dict(type="variable_statement", value=variable_declaration)

    def variable_initializer(self) -> AnyDict | None:
        if self.lookahead.type == "NL":
            return None
        expression = dict()
        return dict(variable_initializer=expression)

    def literal(self) -> AnyDict:
        value = EOF_TOKEN
        if self.lookahead.type == "NUMBER":
            value = self.number_lit()
        elif self.lookahead.type == "STRING":
            value = self.string_lit()
        return dict(type="literal", value=value)

    def number_lit(self) -> AnyDict:
        token = self._consume("NUMBER")
        return dict(type="number", value=int(token.value))

    def string_lit(self) -> AnyDict:
        token = self._consume("STRING")
        return dict(type="string", value=token.value[1:-1])
