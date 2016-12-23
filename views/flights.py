import tkinter as tk
from tkinter import ttk

from views.view import View

class FlightsView(View):
    def __init__(self, parent, *args, **kwargs):
        View.__init__(self, parent, *args, **kwargs)
        l = ttk.Label(self, text="să moară Janeta")
        l.grid(row=0, column=0, sticky='nsew')
        l.config(anchor='center')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)