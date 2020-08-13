import platform

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


@pytest.mark.skipif(platform.system() != 'Windows',
                    reason="Test Windows behavior")
def test_appends_exe_on_windows():
    result = svtgui.append_extension('executable')
    assert result == 'executable.exe'


@pytest.mark.skipif(platform.system() == 'Windows',
                    reason="Test Unix behavior")
def test_appends_exe_on_unix():
    result = svtgui.append_extension('executable')
    assert result == 'executable'
