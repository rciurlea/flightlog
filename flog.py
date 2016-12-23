#!/usr/bin/env python3
# This is a Python 3 app!

import tkinter as tk
from tkinter import ttk
from views import FlightsView, EntitiesView

class FLogApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # window setup
        h, w = 800, 1200
        screen_h = self.winfo_screenheight()
        screen_w = self.winfo_screenwidth()
        self.title("Flight Log")
        self.minsize(400, 200)
        self.geometry('%dx%d+%d+%d' % (w, h, (screen_w - w) / 2, (screen_h - h) / 2))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        if self.tk.call('tk', 'windowingsystem') in ('x11', 'win32'):
            # start maximized
            self.attributes('-zoomed', True)

        # menu bar
        # menu_bar = tk.Menu(self)
        # menu_bar.add_command(label="Hello!")
        # menu_bar.add_command(label="Quit!", command=self.quit)
        # self.config(menu=menu_bar)

        # tab config
        note = ttk.Notebook(self)
        tab1 = ttk.Frame(note)
        tab2 = ttk.Frame(note)
        tab3 = ttk.Frame(note)
        tab4 = ttk.Frame(note)

        note.add(tab1, text = " View / Add Flights ", underline="12")
        note.add(tab2, text = " Duty Times ")
        note.add(tab3, text = " Generate Reports ")
        note.add(tab4, text = " Entities ")
        note.select(tab4)
        note.grid(column=0, row=0, sticky="nsew")
        note.enable_traversal()

        # /tabconfig

        FlightsView(tab1).grid(column=0, row=0, sticky='nsew')
        tab1.columnconfigure(0, weight=1)
        tab1.rowconfigure(0, weight=1)

        ev = EntitiesView(tab4)
        ev.grid(column=0, row=0, sticky='nsew')
        tab4.columnconfigure(0, weight=1)
        tab4.rowconfigure(0, weight=1)
        ev.pf.order('code')
        ev.af.order('icao_code')
        ev.tf.order('name')
        ev.acf.order('registration')
        ev.cf.order('name')
        

        # status bar
        self.status_string = tk.StringVar()
        status_frame = ttk.Frame(self)
        status_frame.grid(row=1, column=0, sticky='nsew')
        status_label = ttk.Label(status_frame, textvariable=self.status_string)
        status_label.grid()
        # /status bar

    def status(self, s):
        self.status_string.set(s)

    def temporary_status(self, s):
        self.status(s)
        self.after(5000, self.status, '')


if __name__ == "__main__":
    app = FLogApp()
    app.mainloop()
