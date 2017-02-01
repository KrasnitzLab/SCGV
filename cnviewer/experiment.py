'''
Created on Feb 1, 2017

@author: lubo
'''
import tkinter as tk
from tkinter import messagebox


class ModalDialog(tk.Toplevel):

    def __init__(self, master=None, **kw):
        tk.Toplevel.__init__(self, master, **kw)
        self.withdraw()

    def show(self):
        self.deiconify()
        self.transient(self.master)
        self.grab_set()


def show():
    messagebox.showerror(
        title="Wrong file/directory type",
        message="Single Cell Genomics data set expected")


def main():
    root = tk.Tk()
    b = tk.Button(root, text='Show', command=show)
    b.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
