import tkinter as tk
from tkinter import ttk, messagebox
from models import Company
from helpers.tree import TreeSorter

class InfoFrame(ttk.Labelframe):
    def __init__(self, parent, *args, **kwargs):
        ttk.Labelframe.__init__(self, parent, *args, **kwargs)

        self.config(text='Infosomethinglol')
        self.config(padding=(10, 5, 10, 10))

        ttk.Label(self, text='some info here in this info pane.').grid()
        
