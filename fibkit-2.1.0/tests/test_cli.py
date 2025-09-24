import sys

import pytest

from fibkit import cli


def run_cli(args):
    argv = ["fibkit", *args]
    with pytest.raises(SystemExit) as exc:
        original = sys.argv
        try:
            sys.argv = argv
            cli.main()
        finally:
            sys.argv = original
    return exc


def test_linrec_negative_n_reports_value_error(capsys):
    exc = run_cli([
        "linrec",
        "--n",
        "-1",
        "--a0",
        "0",
        "--a1",
        "1",
        "--p",
        "1",
        "--q",
        "1",
    ])
    assert exc.value.code == 2
    _, err = capsys.readouterr()
    assert "n must be non-negative integer" in err
