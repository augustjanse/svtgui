import platform

import pytest

import svtgui


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
