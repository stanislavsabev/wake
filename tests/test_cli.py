"""Test CLI entry point."""
from wake import cli


def test_cli(capsys):
    """Test CLI entry point."""
    cli.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello from win-make!\n"
