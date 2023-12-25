from wake.tokenizer import EOF, EOF_TOKEN, Token, Tokenizer
from wake.typedef import AnyDict


class Parser:
    def __init__(self) -> None:
        self.string = ""
        self.tokenizer = Tokenizer()
        self.lookahead = EOF_TOKEN

    def parse(self, string) -> Token:
        self.string = string
        self.tokenizer.string = string
        self.lookahead = self.tokenizer.get_next()
        return self.variables()

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
    def variables(self) -> list[AnyDict]:
        variables = []
        while self.lookahead != "LABEL":
            statement = self.statement()
            variables.append(statement)
        return variables

    def recipes(self) -> list[AnyDict]:
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
