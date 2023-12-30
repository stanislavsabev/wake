from wake.tokenizer import EOF, EOF_TOKEN, Token, Tokenizer
from wake.typedef import AnyDict


EMPTY_PRODUCTION = {"type": "Empty"}


class Parser:
    """Parser for the wakefile."""

    def __init__(self) -> None:
        self.string = ""
        self.tokenizer = Tokenizer()
        self.lookahead = EOF_TOKEN

    def parse(self, string) -> AnyDict:
        """Parses provided string.

        Args:
            string: str to parse.

        Returns:
            A dict with parsed AST.
        """
        self.string = string
        self.tokenizer.string = string

        self.lookahead = self.tokenizer.get_next()
        # return self.variables()
        return {}

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

    # def variables(self) -> list[AnyDict]:
    #     variables = []
    #     while self.lookahead != "LABEL":
    #         statement = self.statement()
    #         variables.append(statement)
    #     return variables

    # def recipes(self) -> list[AnyDict]:
    #     procecures = []
    #     return procecures

    # def statement(self) -> AnyDict:
    #     if self.lookahead == "IDENTIFIER":
    #         return self.variable_statement()
    #     else:
    #         return self.literal()

    def variable_declaration(self) -> AnyDict:
        """Variable declaration production."""
        if self.lookahead.type == "IDENTIFIER":
            name = self._consume("IDENTIFIER")
            declarator = {"type": "Identifier", "name": name.value}
        else:
            raise ValueError(
                f"Invalid token type {self.lookahead.type}, expected identifier."
            )

        self._consume("=")
        initializer = self.variable_initializer()
        result = {
            "type": "VariableDeclaration",
            "value": {
                "type": "VariableDeclarator",
                "id": declarator,
                "init": initializer,
            },
        }
        return result

    def variable_initializer(self) -> AnyDict:
        """Variable initializer production."""
        if self.lookahead.type == "NEWLINE":
            self._consume("NEWLINE")
            return EMPTY_PRODUCTION
        # TODO: [2023/12/26, 12:17:13] Change this to
        # an expression production, after implementing it.
        expression = self.literal()
        return expression

    def literal(self) -> AnyDict:
        """Literal production."""
        result = {"type": "Literal"}
        if self.lookahead.type == "INTEGER":
            token = self._consume("INTEGER")
            result.update({"value": int(token.value), "raw": token.value})
        elif self.lookahead.type == "STRING":
            token = self._consume("STRING")
            result.update({"value": token.value[1:-1], "raw": token.value})
        else:
            raise ValueError(f"Unsupported literal {token.value}")
        return result
