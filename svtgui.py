import tkinter as tk
from subprocess import call

# Very adapted from http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
class SVTGUI:
    def __init__(self, master):
        self.master = master
        master.title("SVTGUI")

        self.label = tk.Label(master, text="Testtext här")
        self.label.pack()

        self.click_button = tk.Button(master, text="Klicka för att kalla funktion", command=self.execute)
        self.click_button.pack()

        self.close_button = tk.Button(master, text="Klicka för att avsluta", command=master.quit)
        self.close_button.pack()

    def execute(self):
        call(["./svtplay-dl"])


root = tk.Tk()
svtgui = SVTGUI(root)
root.mainloop()
