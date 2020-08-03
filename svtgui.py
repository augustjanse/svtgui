import subprocess
import sys
import tkinter as tk


class SVTGUI:
    def __init__(self, master):
        """Initalize a GUI window with checkboxes, a text box and a clickable
        "Download" button.
        """
        self._set_up_window(master)
        self._set_up_input_box()
        self._set_up_checkboxes()
        self._set_up_button()
        self._set_up_output_box()

    def _set_up_window(self, master):
        self.master = master
        self.master.title("SVTGUI")

    def _set_up_input_box(self):
        self.textbox = tk.Text(self.master, height=1, width=100)
        self.textbox.pack()

    def _set_up_checkboxes(self):
        self.subtitles_checked = tk.BooleanVar(value=True)
        self.subtitle_check = tk.Checkbutton(self.master,
                                             text="Subtitles",
                                             variable=self.subtitles_checked)
        self.subtitle_check.pack()

        self.all_episodes_checked = tk.BooleanVar()
        self.all_episodes_check = tk.Checkbutton(
            self.master,
            text="All episodes",
            variable=self.all_episodes_checked)
        self.all_episodes_check.pack()

    def _set_up_button(self):
        self.out = ''
        self.click_button = tk.Button(
            self.master,
            text="Download",
            command=lambda: self.execute(self.subtitles_checked.get(),
                                         self.all_episodes_checked.get(),
                                         self.textbox.get("1.0", "end-1c")))
        self.click_button.pack()

    def _set_up_output_box(self):
        self.details = tk.Text(self.master, height=10, width=100)
        self.details.pack()
        sys.stdout = StdoutRedirector(self.details)

    def execute(self, subtitles_checked, all_episodes_checked, url):
        """Calls svtplay-dl. Uses values from checkboxes and textbox. When
        finished, the indicated files should have been downloaded to the
        file system.
        """
        argument_list = ["svtplay-dl"]

        if subtitles_checked:
            argument_list.extend([
                "--merge-subtitle", "--convert-subtitle-colors",
                "--all-subtitles", "--force"
            ])

        if all_episodes_checked:
            argument_list.extend(["--all-episodes"])

        if url:
            argument_list.append(url)

        print(" ".join(argument_list))
        for line in run_shell_command(argument_list):
            print(line)


# https://stackoverflow.com/a/4417735/1729441
def run_shell_command(args):
    """Calls the given shell command, then yields one line at a time of
    the combined stdout/stderr output.
    """

    popen = subprocess.Popen(args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True)
    for line in iter(popen.stdout.readline, ""):
        yield line
    popen.stdout.close()
    ret = popen.wait()

    if ret:
        raise subprocess.CalledProcessError(ret, args)


# https://stackoverflow.com/q/18517084/1729441
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert('end', string)
        self.text_space.see('end')
        self.text_space.update_idletasks()


root = tk.Tk()
svtgui = SVTGUI(root)
root.mainloop()
