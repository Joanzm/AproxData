from Parser.celldataparser_xlr import XLRCellDataParser
from View.frame_scrollable import ScrollableFrame
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from threading import *

if __name__ == "__main__":
    """
    Starts the tkinter GUI
    """

    def load_files():
        filetypes = [('Cell Data', '*.xls')]
        files = fd.askopenfilenames(
            title = 'Lade Zelldaten',
            initialdir='/',
            filetypes=filetypes)

        labels = [0 for a in range(len(files))]
        for i in range(len(files)):
            if files[i] != "" and files[i].endswith('.xls'):
                labels[i] = label = ttk.Label(frame.scrollable_frame, text=files[i], foreground="black")
                label.pack()

        for i in range(len(files)):
            if files[i] != "" and files[i].endswith('.xls'):
                labels[i].config(foreground="red")
                p = XLRCellDataParser()
                p.load_book(files[i])
                p.load_sheets()
                labels[i].config(foreground="green")

    root = tk.Tk()

    #configure grid
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0, weight=2);
    root.rowconfigure(1, weight=0)
    root.rowconfigure(2, weight=2)

    frame = ScrollableFrame(root)
    frame.grid(column=0,row=0,sticky=tk.N+tk.S+tk.W+tk.E)

    label_1 = ttk.Label(root, text="reservation_1")
    label_1.grid(column=1,row=0,rowspan=2,sticky=tk.N+tk.S+tk.W+tk.E)
    
    button_1 = ttk.Button(root, text="Lade Daten", command=lambda: Thread(target = load_files).start())
    button_1.grid(column=0,row=1,sticky=tk.N+tk.S+tk.W+tk.E,padx=5,pady=5)

    label_2 = ttk.Label(root, text="reservation_2")
    label_2.grid(column=0,row=2,sticky=tk.N+tk.S+tk.W+tk.E)

    label_3 = ttk.Label(root, text="reservation_3")
    label_3.grid(column=1,row=2,sticky=tk.N+tk.S+tk.W+tk.E)
    
    root.mainloop()