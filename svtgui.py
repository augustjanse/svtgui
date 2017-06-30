import tkinter as tk
from subprocess import call

# Very adapted from http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
class SVTGUI:
    def __init__(self, master):
        self.master = master
        master.title("SVTGUI")

        self.textbox = tk.Text(master, height=1, width=100)
        self.textbox.pack()

        self.subtitles_checked = tk.BooleanVar()
        self.subtitle_check = tk.Checkbutton(master, text="Subtitles", variable=self.subtitles_checked)
        self.subtitle_check.pack()

        self.click_button = tk.Button(master, text="Klicka för att kalla funktion", command=self.execute)
        self.click_button.pack()

        self.close_button = tk.Button(master, text="Klicka för att avsluta", command=master.quit)
        self.close_button.pack()

    def execute(self):
        argument_list = ["./svtplay-dl"]

        if self.subtitles_checked.get():
            argument_list.extend(["-M", "--convert-subtitle-colors", "--all-subtitles"])

        url = self.textbox.get("1.0", "end-1c")
        if url:
            argument_list.append(url)

        print(" ".join(argument_list))
        call(argument_list)

root = tk.Tk()
svtgui = SVTGUI(root)
root.mainloop()
