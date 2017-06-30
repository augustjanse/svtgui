import tkinter as tk
from subprocess import call

# Very adapted from http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
class SVTGUI:
    def __init__(self, master):
        self.master = master
        master.title("SVTGUI")

        self.textbox = tk.Text(master, height=1, width=100)
        self.textbox.pack()

        self.subtitles_checked = tk.BooleanVar(value=True)
        self.subtitle_check = tk.Checkbutton(master, text="Subtitles", variable=self.subtitles_checked)
        self.subtitle_check.pack()

        self.all_episodes_checked = tk.BooleanVar()
        self.all_episodes_check = tk.Checkbutton(master, text="All episodes", variable=self.all_episodes_checked)
        self.all_episodes_check.pack()

        self.click_button = tk.Button(master, text="Download", command=self.execute)
        self.click_button.pack()

    def execute(self):
        argument_list = ["./svtplay-dl"]

        if self.subtitles_checked.get():
            argument_list.extend(["--merge-subtitle", "--convert-subtitle-colors", "--all-subtitles"])

        if self.all_episodes_checked.get():
            argument_list.extend(["--all-episodes"])

        url = self.textbox.get("1.0", "end-1c")
        if url:
            argument_list.append(url)

        print(" ".join(argument_list))
        call(argument_list)

root = tk.Tk()
svtgui = SVTGUI(root)
root.mainloop()
