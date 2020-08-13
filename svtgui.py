"""Starts the SVTGUI graphical application."""

import os
import platform
import queue
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog

import svtplay_dl


class SVTGUI():  # pylint: disable=too-few-public-methods
    """The main window of the application."""
    def __init__(self, master):
        """Initalize a GUI window with checkboxes, a text box and a clickable
        "Download" button.
        """
        self.q = queue.Queue()
        master.after(100, self.check_queue)

        self._set_up_window(master)
        self._set_up_input_box()
        self._set_up_checkboxes()
        self._set_up_output_directory_box()
        self._set_up_button()
        self._set_up_output_box()

    def _set_up_window(self, master):
        self.master = master
        self.master.title("SVTGUI")

    def _set_up_input_box(self):
        self.textbox = tk.Entry(self.master, width=100)
        self.textbox.bind('<Return>', lambda event: self.start_download())
        self.textbox.bind('<Control-a>', select_all)
        self.textbox.pack()

    def _set_up_checkboxes(self):
        self.subtitles_checked = tk.BooleanVar(value=True)
        tk.Checkbutton(self.master,
                       text="Subtitles",
                       variable=self.subtitles_checked).pack()

        self.all_episodes_checked = tk.BooleanVar(value=False)
        tk.Checkbutton(self.master,
                       text="All episodes",
                       variable=self.all_episodes_checked).pack()

    def _set_up_output_directory_box(self):
        self.output_directory_box = tk.Entry(self.master, width=80)
        self.output_directory_box.bind('<Control-a>', select_all)
        self.output_directory_box.pack()

        tk.Button(self.master,
                  text="Browse...",
                  command=lambda: self.output_directory_box.insert(
                      'end', filedialog.askdirectory())).pack()

    def _set_up_button(self):
        self.out = ''

        self.click_button = tk.Button(self.master,
                                      text="Download",
                                      command=self.start_download)

        self.click_button.pack()

    def _set_up_output_box(self):
        self.details = tk.Text(self.master, height=10, width=100)
        self.details.pack()
        sys.stdout = StdoutRedirector(self.details)

    def start_download(self):
        """Calls execute with the contents of checkboxes and input box."""
        self.q.put(lambda: execute(self.subtitles_checked.get(
        ), self.all_episodes_checked.get(), self.textbox.get(),
                                   self.output_directory_box.get()))

    # http://stupidpythonideas.blogspot.com/2013/10/
    # why-your-gui-app-freezes.html
    def check_queue(self):
        while True:
            try:
                task = self.q.get(block=False)
            except queue.Empty:
                break
            else:
                root.after_idle(task)
        root.after(100, self.check_queue)


def execute(subtitles_requested, all_episodes_requested, url,
            output_directory):
    """Calls svtplay-dl. If subtitles_requested, subtitles are downloaded
    and merged. If all_episodes_requested, all episodes of the series are
    downloaded. When finished, the indicated files should have been
    downloaded to the file system.
    """
    argument_list = [resource_path(append_extension("svtplay-dl"))]

    if subtitles_requested:
        argument_list.extend([
            "--merge-subtitle", "--convert-subtitle-colors", "--all-subtitles",
            "--force"
        ])

    if all_episodes_requested:
        argument_list.append("--all-episodes")

    if url:
        argument_list.append(url)

    if output_directory:
        argument_list.extend(['--output', output_directory])

    print(" ".join(argument_list))
    run_shell_command(argument_list)


# https://stackoverflow.com/a/4417735/1729441
def run_shell_command(args):
    """Calls the given shell command, then prints one line at a time of
    the combined stdout/stderr output.
    """

    popen = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True)
    for line in iter(popen.stdout.readline, ""):
        print(line)
    popen.stdout.close()
    ret = popen.wait()

    if ret:
        raise subprocess.CalledProcessError(ret, args)


# https://stackoverflow.com/a/53640777/1729441
def select_all(event):
    """Selects all text in the widget indicated by the event.
    Returns 'break' to stop event propagation (if bound to a key press).
    """
    event.widget.select_range(0, 'end')
    event.widget.icursor('end')
    return 'break'


def append_extension(binary):
    """Appends the appropriate extension to the name of an executable,
    depending on the OS."""
    system = platform.system()

    return binary + '.exe' if system == 'Windows' else binary


# https://stackoverflow.com/a/13790741/1729441
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class StdoutRedirector():
    # https://stackoverflow.com/q/18517084/1729441
    """A stdout replacement that instead writes to the given tk Text object."""
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        """When written to (by print statements), insert the output to the
        end of self.text_space, jump there, and update."""
        self.text_space.insert('end', string)
        self.text_space.see('end')
        self.text_space.update_idletasks()

    def flush(self):
        """Called when window is closed: do nothing."""


if __name__ == "__main__":
    root = tk.Tk()
    svtgui = SVTGUI(root)
    root.mainloop()
