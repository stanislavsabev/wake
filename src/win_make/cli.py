"""CLI entry point."""
import os
import sys

from win_make import engine, parser

FILE_NAME = "win-makefile"


def main():
    """CLI entry point."""
    if not os.path.isfile(FILE_NAME):
        raise FileNotFoundError(f"Current directory does not contain '{FILE_NAME}'")

    if len(sys.argv) < 2:
        raise ValueError("Missing label name!")

    with open(FILE_NAME, "r", encoding="utf-8") as fd:
        contents = fd.read()

    parser_obj = parser.Parser()
    model: parser.Model = parser_obj.parse_makefile(contents)
    if not model.labels:
        raise ValueError(f"'{FILE_NAME}' is missing label definitions.")

    label_name = sys.argv[1]

    for label in model.labels:
        if label_name in [label.name, label.short]:
            break
    else:
        raise ValueError(f"Could not find label '{label_name}'")

    args = sys.argv[2:]
    if args:
        label = parser_obj.parse_args(label, args)

    engine.exec_label(label, args, dict(**os.environ.items()))

    print(f"found {label.short}/{label.name=}")
