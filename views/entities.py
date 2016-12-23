import tkinter as tk
from tkinter import ttk, messagebox

from views.view import View
from views.pilots import PilotsFrame
from views.airfields import AirfieldsFrame
from views.types import TypesFrame
from views.aircraft import AircraftFrame
from views.companies import CompaniesFrame
from views.info import InfoFrame

class EntitiesView(View):
    def __init__(self, parent, *args, **kwargs):
        View.__init__(self, parent, *args, **kwargs)

        # general view setup
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.config(padding=(10,10,10,10))
        # /setup

        # pilot section
        self.pf = PilotsFrame(self)
        self.pf.grid(row=0, column=0, sticky='nsew', padx=(0,5))
        # /pilot section

        # airfields section
        self.af = AirfieldsFrame(self)
        self.af.grid(row=1, column=0, sticky='nsew', padx=(0,5), pady=(10,0))
        # /airfields

        # aircraft section
        self.acf = AircraftFrame(self)
        self.acf.grid(row=0, column=1, sticky='nsew', padx=(5,5))
        # /aircraft

        # types section
        self.tf = TypesFrame(self)
        self.tf.grid(row=1, column=1, sticky='nsew', padx=(5,5), pady=(10,0))
        # /types

        # companies section
        self.cf = CompaniesFrame(self)
        self.cf.grid(row=0, column=2, sticky='nsew', padx=(5,0))
        # /companies

        # statistics frame
        self.info = InfoFrame(self)
        self.info.grid(row=1, column=2, sticky='nsew', padx=(5,0), pady=(10,0))
        # /statistics