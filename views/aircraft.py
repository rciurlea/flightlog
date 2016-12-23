import tkinter as tk
from tkinter import ttk, messagebox
from models import Pilot, Aircraft, ACType
from helpers.tree import TreeSorter

class AircraftFrame(TreeSorter, ttk.Labelframe):
    def __init__(self, parent, *args, **kwargs):
        ttk.Labelframe.__init__(self, parent, *args, **kwargs)
        TreeSorter.__init__(self)

        self.registration_var = tk.StringVar()
        self.type_var = tk.StringVar()
        self.ifr_var = tk.StringVar()

        self.config(text='Aircraft')
        self.config(padding=(10, 5, 10, 10))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=('registration', 'type', 'instrument_capable'), selectmode='browse')
        self.tree.column('registration', width=25, anchor='center')
        self.tree.column('type', width=50, anchor='center')
        self.tree.column('instrument_capable', width=50, anchor='center')
        self.tree['show'] = 'headings'
        self.tree.heading('registration', text='Registration', command=lambda: self.order('registration'))
        self.tree.heading('type', text='Type', command=lambda: self.order('type'))
        self.tree.heading('instrument_capable', text='IFR Capable', command=lambda: self.order('instrument_capable'))
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        s.grid(row=0, column=1, sticky='ns', pady=(0, 10))
        self.tree['yscrollcommand'] = s.set

        sf = ttk.Frame(self)
        sf.grid(row=1, column=0, columnspan=2, sticky='nsew')
        sf.columnconfigure(0, weight=1)
        sf.columnconfigure(1, weight=1)
        ttk.Button(sf, text="Add Aircraft...", command=self.add_wnd).grid(row=0, column=0, padx=(0,5), sticky='nsew')
        ttk.Button(sf, text="Delete", command=self.remove_ac).grid(row=0, column=1, padx=(5,0), sticky='nsew')

    
    def load_data(self, order_by='registration', ascending=True):
        if order_by == 'registration':
            if ascending:
                data = Aircraft.select().order_by(Aircraft.registration)
            else:
                data = Aircraft.select().order_by(Aircraft.registration.desc())
        elif order_by == 'type':
            if ascending:
                data = Aircraft.select().join(ACType).order_by(ACType.name)
            else:
                data = Aircraft.select().join(ACType).order_by(-ACType.name)
        else:
            if ascending:
                data = Aircraft.select().order_by(Aircraft.instrument_capable)
            else:
                data = Aircraft.select().order_by(Aircraft.instrument_capable.desc())

        for ac in data:
            self.tree.insert('', 'end', str(ac.id), values=(ac.registration, ac.actype.name, ac.instrument_capable))


    def remove_ac(self):
        for i in self.tree.selection():
            guy = Aircraft.get(Aircraft.id == int(i))
            ans = messagebox.askyesno(title='Remove aircraft?', 
                                message='Are you sure you want to remove %s from the database?' % (guy.registration,))
            if ans:
                self.tree.delete(i)
                self._root().temporary_status("Removed %s." % (guy.registration,))
                guy.delete_instance()


    def add_wnd(self):
        root = self._root()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        rh = root.winfo_height()
        w, h = 300, 100
        self.form = tk.Toplevel()
        self.form.title('Add Aircraft')
        self.form.geometry('+%d+%d' % (rx + rw/2 - 100, ry + rh/2 - 100))

        f = ttk.Frame(self.form, padding=(10,10,10,10))
        f.pack()

        ttk.Label(f, text="Registration", anchor="e").grid(row=0, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        f_reg = ttk.Entry(f, width=10, textvariable=self.registration_var)
        f_reg.grid(row=0, column=1, sticky='nsew', pady=(0,5))
        f_reg.focus_set()

        self.actypes = {}
        for t in ACType.select():
            self.actypes[t.manufacturer + ' ' + t.name] = t.id
        print(self.actypes)

        types_list = [t.manufacturer + ' ' + t.name for t in ACType.select().order_by(ACType.manufacturer, ACType.name)]

        ttk.Label(f, text='Type', anchor="e").grid(row=1, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        f_type = ttk.Combobox(f, textvariable=self.type_var, state='readonly')
        f_type['values'] = types_list
        f_type.grid(row=1, column=1, sticky='nsew', pady=(0,5))

        ttk.Label(f, text='IFR Capable', anchor="e").grid(row=2, column=0, sticky='nsew', padx=(0,10))
        f_ifr = ttk.Checkbutton(f, variable=self.ifr_var, onvalue='Yes', offvalue='No')
        f_ifr.grid(row=2, column=1, sticky='nsew')

        f2 = ttk.Frame(f)
        f2.grid(row=3, column=0, columnspan=2, pady=(10,0))
        ttk.Button(f2, text="Save", command=self.save_data).grid(row=0, column=0, padx=(0,5))
        ttk.Button(f2, text="Cancel", command=self.form.destroy).grid(row=0, column=1, padx=(5,0))

        self.form.transient(root)
        self.form.grab_set()
        root.wait_window(self.form)


    def save_data(self):
        registration = self.registration_var.get().strip().upper()
        actype = self.actypes.get(self.type_var.get(), None)
        print(self.type_var.get(), actype)
        ifr_capable = self.ifr_var.get()

        if registration == '' or actype is None:
            messagebox.showinfo(message="Registration and type can't be empty!")
        else:
            try:
                Aircraft.create(registration=registration, actype=actype, instrument_capable=ifr_capable)
                self.ifr_var.set('No')
                self.type_var.set('')
                self.registration_var.set('')

                self.form.destroy()
                self.clear_tree()
                self.load_data()
                self._root().temporary_status('Added %s.' % (registration, ))
            except Exception as e:
                messagebox.showinfo(message='The code is already in use!')
                print(e)

