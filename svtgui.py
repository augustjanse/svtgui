import sys
import tkinter as tk
import subprocess


class SVTGUI:
    def __init__(self, master):
        """Initalize a GUI window with checkboxes, a text box and a clickable
        "Download" button.
        """
        self.master = master
        master.title("SVTGUI")

        self.textbox = tk.Text(master, height=1, width=100)
        self.textbox.pack()

        self.subtitles_checked = tk.BooleanVar(value=True)
        self.subtitle_check = tk.Checkbutton(master,
                                             text="Subtitles",
                                             variable=self.subtitles_checked)
        self.subtitle_check.pack()

        self.all_episodes_checked = tk.BooleanVar()
        self.all_episodes_check = tk.Checkbutton(
            master, text="All episodes", variable=self.all_episodes_checked)
        self.all_episodes_check.pack()

        self.out = ''
        self.click_button = tk.Button(
            master,
            text="Download",
            command=lambda: self.execute(self.subtitles_checked.get(),
                                         self.all_episodes_checked.get(),
                                         self.textbox.get("1.0", "end-1c")))
        self.click_button.pack()

        self.details = tk.Text(master, height=10, width=100)
        self.details.pack()

        self.update_output(self.details, 0)

    def execute(self, subtitles_checked, all_episodes_checked, url):
        """Calls svtplay-dl. Uses values from checkboxes and textbox. When
        finished, the indicated files should have been downloaded to the
        file system.
        """
        argument_list = ["svtplay-dl"]

        if subtitles_checked:
            argument_list.extend([
                "--merge-subtitle", "--convert-subtitle-colors",
                "--all-subtitles"
            ])

        if all_episodes_checked:
            argument_list.extend(["--all-episodes"])

        if url:
            argument_list.append(url)

        print(" ".join(argument_list))
        for line in self.run_shell_command(argument_list):
            self.out = self.out + line

    def update_output(self, textbox, line):
        """Update the output textbox every half second."""
        lines = self.out.strip().split('\n')

        if lines == ['']:
            lines = []

        new = lines[line:]

        if new:
            new_lines = '\n'.join(new) + '\n'
        else:
            new_lines = ''

        textbox.insert(tk.END, new_lines)
        textbox.after(100, lambda: self.update_output(textbox, len(lines)))

    # https://stackoverflow.com/a/4417735/1729441
    def run_shell_command(self, args):
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


root = tk.Tk()
svtgui = SVTGUI(root)
root.mainloop()
