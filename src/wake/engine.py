"""Command execution engine."""
from collections import namedtuple

from wake import typedef

Std = namedtuple("Std", ["in_", "out", "err"])


def cmd(text: str) -> Std:
    """Executes shell command.

    Args:
        text: A string with shell command to execute
    Returns:
        standard stream - in, out, err
    """
    return Std(None, None, None)


def exec_label(
    production: typedef.AnyDict, args: list[str], environ: dict[str, str]
) -> None:
    """Executes all shell commands in label contents.

    Args:
        label: A Label to execute
        args: Command line args passed, sys.argv
        environ: Environment variables, os.environ

    Returns:
        standard stream - in, out, err
    """
    pass
