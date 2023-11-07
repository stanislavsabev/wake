"""Parsing and tokenizing module."""
import re
from collections import namedtuple

SHELLS = ["cmd", "powershell"]


WS = r"\s*"
WS_EXCEPT_NEWLINE = r"[^\S\n]"
NON_WS = r"\S"
COMMENT = r"#.*$"
COLON = r":"
NUMBER = r"\d+"
EQ = r":?="
LPAREN = r"\("
RPAREN = r"\)"
SHELL = r"^shell"
DOUBLE_Q = r"\""
STRING = r"\"(?:\"\")*\""
# No numbers and no _ or - at the beginning and the end of the word
LOW_WORD = r"\b[a-z][a-z0-9_-]*[a-z]\b"
LABEL_NAME = LOW_WORD + COLON
VAR_NAME = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"  # Standard variable name
ENV_VAR_NAME = r"\$\$" + VAR_NAME

LEN = r"@len"
PARAMS = r"@params"
FLAGS = r"@flags"
DOC = r"@doc"

model_spec = {
    "WHITESPACE": WS,
    "=": EQ,
    "shell": SHELL,
    "label": LABEL_NAME,
    "variable": VAR_NAME,
    "lowercase_word": LOW_WORD,
}

var_value_spec = {
    "WHITESPACE": WS,
    "COMMENT": COMMENT,
    "WHITESPACE_EXCEPT_NEWLINE": WS_EXCEPT_NEWLINE,
    "STRING": STRING,
    "NON_WHITESPACE": NON_WS,
}

common_spec = {
    "WHITESPACE": WS,
    "=": EQ,
    "COMMENT": COMMENT,
    "lowercase_word": LOW_WORD,
    "params": PARAMS + COLON,
    "flags": FLAGS + COLON,
    "doc": DOC + COLON,
    "len": LEN,
    "variable": VAR_NAME,
}

Token = namedtuple("Token", ["typ", "val"], defaults=["", ""])
EOF_TOKEN = Token(typ="EOF", val="")


# class Statement:
#     """Statement class used in parser."""

#     typ: str
#     text: str | "Statement" | "StatementList"


# class StatementList:
#     """StatementList class used in parser."""

#     statements: "Statement" | "StatementList"


class Flag:
    """Flag class used in parser."""

    name: str
    short: str | None
    defined: bool = False


class Param:
    """Param class used in parser."""

    name: str
    short: str | None
    val: list[str]
    default: str | None
    defined: bool = False


class Label:
    """Label class used in parser."""

    name: str
    short: str | None

    flags: list[Flag]
    params: list[Param]
    doc: str | None

    contents: list[str]


class Model:
    """Model class used in parser."""

    shell: str
    vars_: dict[str, str | list[str]]
    labels: list[Label]


class Tokenizer:
    """VBA Tokenizer."""

    def __init__(self) -> None:
        """Create Tokenizer."""
        self._contents = ""
        self._spec = common_spec
        self._cursor = 0

    def set_contents(self, contents: str) -> None:
        """Set tokenizer contents."""
        self._contents = contents

    def get_next_token(self, ignore_ws: bool = True, spec: dict[str, str] | None = None) -> Token:
        """Gets the next token in the input string.

        Returns:
            Token: The next token or EOF_TOKEN
                if there are no more tokens.

        Raises:
            SyntaxError: Unexpected token.
        """
        if not self.has_more_tokens():
            return EOF_TOKEN

        if not spec:
            spec = self._spec

        contents = self._contents[self._cursor :]
        for typ, pattern in spec.items():
            match = self._match(pattern, contents)
            if not match:
                continue

            if ignore_ws and typ in ["WHITESPACE", "COMMENT"]:
                continue

            return Token(
                typ=typ,
                val=match,
            )

        before = max(0, self._cursor - 5)
        after = min(self._cursor + 5, len(self._contents))
        line = self._contents[before:after]
        err_line = 4 * "~" * bool(before) + "^^" + 4 * "~" * bool(after)
        err_line = "\n".join([line, err_line])
        raise SyntaxError(f"Unexpected token: at pos {self._cursor:N}\n{err_line}")

    def _match(self, pattern: str, string: str) -> str | None:
        match = re.match(pattern, string, flags=re.IGNORECASE)
        if match:
            self._cursor += len(match[0])
            return match[0]
        return None

    def has_more_tokens(self) -> bool:
        """Checks if there are more tokens in the input string.

        Returns:
            bool: True if cursor is not at the end of the input,
                False otherwise.
        """
        return self._cursor < len(self._contents)


class Parser:
    """Parser for wakefile."""

    def __init__(self) -> None:
        self.tokenizer = Tokenizer()
        self.lookahead = EOF_TOKEN

    def parse_makefile(self, contents: str) -> Model:
        """Parse wake contents.

        Args:
            contents (str): A string with file contents

        Returns:
            A Model: wake model
        """
        model = Model()
        self.tokenizer.set_contents(contents)
        lookahead = self.tokenizer.get_next_token(spec=model_spec)

        while True:
            if lookahead == EOF_TOKEN:
                break
            if lookahead.typ == "shell":
                self.consume(EQ)
                token = self.consume("lowercase_word")
                if token.val not in SHELLS:
                    raise ValueError(f"Unsupported shell name '{token.val}'")
                model.shell = token.val
            elif lookahead.typ == "variable":
                self.consume(EQ)
                var_val = self.variable_value()
                model.vars_[lookahead.val] = var_val
            elif lookahead.typ == "label":
                pass
            else:
                raise ValueError("Invalid token. Expected 'label', 'shell' or 'variable'")
        return model

    def variable_value(self) -> str | list[str]:
        """Read variable value.

        Returns:
            str or list[str]
        """
        var_val: list[str] = []
        is_last_whitespace = False
        lookahead = self.tokenizer.get_next_token(ignore_ws=False, spec=var_value_spec)
        while True:
            if lookahead == EOF_TOKEN:
                raise SyntaxError("Expected variable, got 'End of Input'")

            token = self.consume(lookahead.typ)
            if token.typ in ["COMMENT", "WS"]:
                break

            if lookahead.typ in ["STRING", "NON_WHITESPACE"]:
                is_last_whitespace = False
                var_val.append(token.val)
            if lookahead.typ == "WHITESPACE_EXCEPT_NEWLINE" and var_val:
                var_val.append(token.val)
                is_last_whitespace = True

        if not var_val:
            raise SyntaxError(f"Expected shell value, got '{lookahead.typ}'")
        if is_last_whitespace:
            var_val.pop()
        if len(var_val) == 1:
            return var_val[0]
        return var_val

    def parse_args(self, label: Label, args: list[str]) -> Label:
        """Parse command line args, match with label variables and assign."""
        return label

    def consume(self, token_type: str, spec: dict[str, str] | None = None) -> Token:
        """Consumes token of particular type.

        Args:
            token_type (str): Token type to consume.
            spec (dict[str, str] | None):
        Raises:
            SyntaxError: Unexpected end of input, if there are no more tokens.
            SyntaxError: Unexpected token.

        Returns:
            Token: Consumed token.
        """
        token = self.lookahead
        if token == EOF_TOKEN:
            raise SyntaxError(f"Expected token '{token_type}', got 'End of Input'")

        if token.typ != token_type:
            raise SyntaxError(f" Expected token '{token_type}', got '{token.typ}'.")

        self.lookahead = self.tokenizer.get_next_token(spec=spec)
        return token
