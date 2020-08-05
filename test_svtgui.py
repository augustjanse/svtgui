import pytest

import svtgui


def test_yields_single_output():
    lines = []
    for line in svtgui.run_shell_command(["echo", "test"]):
        lines.append(line)

    assert lines[0].strip() == "test"
    assert lines == ["test\n"]


def test_yields_high_index_output():
    lines = []
    command = ["shuf", "-r", "-i", "1-100", "-n", "1000"]
    for line in svtgui.run_shell_command(command):
        lines.append(line)

    result = int(lines[867].strip())
    assert 1 <= result <= 1000
