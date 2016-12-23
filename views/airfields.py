import tkinter as tk
from tkinter import ttk, messagebox
from models import Airport
from helpers.tree import TreeSorter

class AirfieldsFrame(TreeSorter, ttk.Labelframe):
    def __init__(self, parent, *args, **kwargs):
        ttk.Labelframe.__init__(self, parent, *args, **kwargs)
        TreeSorter.__init__(self)

        self.form_code_entry = tk.StringVar()
        self.form_name_entry = tk.StringVar()

        self.config(text='Airfields')
        self.config(padding=(10, 5, 10, 10))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=('icao_code', 'name'), selectmode='browse')
        self.tree.column('icao_code', anchor='center', width=30)
        self.tree.column('name', anchor='center', width=50)
        self.tree['show'] = 'headings'
        self.tree.heading('icao_code', text='ICAO Code', command=lambda: self.order('icao_code'))
        self.tree.heading('name', text='Name', command=lambda: self.order('name'))
        self.tree.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        s.grid(row=0, column=1, sticky='ns', pady=(0, 10))
        self.tree['yscrollcommand'] = s.set

        sf = ttk.Frame(self)
        sf.grid(row=1, column=0, columnspan=2, sticky='nsew')
        sf.columnconfigure(0, weight=1)
        sf.columnconfigure(1, weight=1)
        ttk.Button(sf, text="Add Airfield...", command=self.add_af_wnd).grid(row=0, column=0, padx=(0,5), sticky='nsew')
        ttk.Button(sf, text="Delete", command=self.remove_af).grid(row=0, column=1, padx=(5,0), sticky='nsew')

    
    def load_data(self, order_by='icao_code', ascending=True):
        if order_by == 'icao_code':
            if ascending:
                data = Airport.select().order_by(Airport.icao_code)
            else:
                data = Airport.select().order_by(Airport.icao_code.desc())
        else:
            if ascending:
                data = Airport.select().order_by(Airport.name)
            else:
                data = Airport.select().order_by(Airport.name.desc())


        for a in data:
            self.tree.insert('', 'end', str(a.id), values=(a.icao_code, a.name))


    def remove_af(self):
        for i in self.tree.selection():
            ap = Airport.get(Airport.id == int(i))
            ans = messagebox.askyesno(title='Remove airfield?', 
                                message='Are you sure you want to remove %s from the database?' % (ap.name, ))
            if ans:
                self.tree.delete(i)
                self._root().temporary_status("Removed %s." % (ap.name, ))
                ap.delete_instance()


    def add_af_wnd(self):
        root = self._root()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        rh = root.winfo_height()
        w, h = 300, 100
        self.form = tk.Toplevel()
        self.form.title('Add Airfield')
        self.form.geometry('+%d+%d' % (rx + rw/2 - 100, ry + rh/2 - 100))

        f = ttk.Frame(self.form, padding=(10,10,10,10))
        f.pack()
        ttk.Label(f, text="Airfield Name", anchor="e").grid(row=0, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        fn = ttk.Entry(f, width=10, textvariable=self.form_name_entry)
        fn.grid(row=0, column=1, sticky='nsew', pady=(0,5))
        fn.focus_set()
        ttk.Label(f, text='ICAO Code', anchor="e").grid(row=1, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        fc = ttk.Entry(f, width=10, textvariable=self.form_code_entry)
        fc.grid(row=1, column=1, sticky='nsew', pady=(0,5))
        f2 = ttk.Frame(f)
        f2.grid(row=2, column=0, columnspan=2, pady=(10,0))
        ttk.Button(f2, text="Save", command=self.save_af).grid(row=0, column=0, padx=(0,5))
        ttk.Button(f2, text="Cancel", command=self.form.destroy).grid(row=0, column=1, padx=(5,0))

        self.form.transient(root)
        self.form.grab_set()
        root.wait_window(self.form)


    def save_af(self):
        code = self.form_code_entry.get().strip().upper()
        name = self.form_name_entry.get().strip()

        if name == '':
            messagebox.showinfo(message="Airfield name can't be empty!")
        else:
            try:
                Airport.create(icao_code=code, name=name)
                self.form_code_entry.set('')
                self.form_name_entry.set('')

                self.form.destroy()
                self.clear_tree()
                self.load_data()
                self._root().temporary_status('Added %s %s.' % (code, name))
            except:
                messagebox.showinfo(message='The code or name are already in use!')
