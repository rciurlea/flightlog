import tkinter as tk
from tkinter import ttk, messagebox
from models import Pilot
from helpers.tree import TreeSorter

class PilotsFrame(TreeSorter, ttk.Labelframe):
    def __init__(self, parent, *args, **kwargs):
        ttk.Labelframe.__init__(self, parent, *args, **kwargs)
        TreeSorter.__init__(self)

        self.form_code_entry = tk.StringVar()
        self.form_fn_entry = tk.StringVar()
        self.form_ln_entry = tk.StringVar()

        self.config(text='Pilots')
        self.config(padding=(10, 5, 10, 10))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=('code', 'first_name', 'last_name'), selectmode='browse')
        self.tree.column('code', width=25, anchor='center')
        self.tree.column('first_name', width=50, anchor='center')
        self.tree.column('last_name', width=50, anchor='center')
        self.tree['show'] = 'headings'
        self.tree.heading('code', text='Code', command=lambda: self.order('code'))
        self.tree.heading('first_name', text='First Name', command=lambda: self.order('first_name'))
        self.tree.heading('last_name', text='Last Name', command=lambda: self.order('last_name'))
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        s.grid(row=0, column=1, sticky='ns', pady=(0, 10))
        self.tree['yscrollcommand'] = s.set

        sf = ttk.Frame(self)
        sf.grid(row=1, column=0, columnspan=2, sticky='nsew')
        sf.columnconfigure(0, weight=1)
        sf.columnconfigure(1, weight=1)
        ttk.Button(sf, text="Add Pilot...", command=self.add_pilot_wnd).grid(row=0, column=0, padx=(0,5), sticky='nsew')
        ttk.Button(sf, text="Delete", command=self.remove_pilot).grid(row=0, column=1, padx=(5,0), sticky='nsew')

    
    def load_data(self, order_by='code', ascending=True):
        if order_by == 'code':
            if ascending:
                data = Pilot.select()
            else:
                data = Pilot.select().order_by(Pilot.code.desc())
        elif order_by == 'first_name':
            if ascending:
                data = Pilot.select().order_by(Pilot.first_name)
            else:
                data = Pilot.select().order_by(Pilot.first_name.desc())
        else:
            if ascending:
                data = Pilot.select().order_by(Pilot.last_name)
            else:
                data = Pilot.select().order_by(Pilot.last_name.desc())

        for pilot in data:
            self.tree.insert('', 'end', str(pilot.id), values=(pilot.code, pilot.first_name, pilot.last_name))


    def remove_pilot(self):
        for i in self.tree.selection():
            guy = Pilot.get(Pilot.id == int(i))
            ans = messagebox.askyesno(title='Remove pilot?', 
                                message='Are you sure you want to remove %s %s from the database?' % (guy.first_name, guy.last_name))
            if ans:
                self.tree.delete(i)
                self._root().temporary_status("Removed %s %s." % (guy.first_name, guy.last_name))
                guy.delete_instance()


    def add_pilot_wnd(self):
        root = self._root()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        rh = root.winfo_height()
        w, h = 300, 100
        self.form = tk.Toplevel()
        self.form.title('Add Pilot')
        self.form.geometry('+%d+%d' % (rx + rw/2 - 100, ry + rh/2 - 100))

        f = ttk.Frame(self.form, padding=(10,10,10,10))
        f.pack()
        ttk.Label(f, text="First Name", anchor="e").grid(row=0, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        fn = ttk.Entry(f, width=10, textvariable=self.form_fn_entry)
        fn.grid(row=0, column=1, sticky='nsew', pady=(0,5))
        fn.focus_set()
        ttk.Label(f, text='Last Name', anchor="e").grid(row=1, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        ln = ttk.Entry(f, width=10, textvariable=self.form_ln_entry)
        ln.grid(row=1, column=1, sticky='nsew', pady=(0,5))
        ttk.Label(f, text='Code', anchor="e").grid(row=2, column=0, sticky='nsew', padx=(0,10))
        c = ttk.Entry(f, width=10, textvariable=self.form_code_entry)
        c.grid(row=2, column=1, sticky='nsew')
        f2 = ttk.Frame(f)
        f2.grid(row=3, column=0, columnspan=2, pady=(10,0))
        ttk.Button(f2, text="Save", command=self.save_pilot).grid(row=0, column=0, padx=(0,5))
        ttk.Button(f2, text="Cancel", command=self.form.destroy).grid(row=0, column=1, padx=(5,0))

        self.form.transient(root)
        self.form.grab_set()
        root.wait_window(self.form)


    def save_pilot(self):
        code = self.form_code_entry.get().strip().upper()
        fn = self.form_fn_entry.get().strip()
        ln = self.form_ln_entry.get().strip()

        if fn == '' or ln == '':
            messagebox.showinfo(message="First name and last name can't be empty!")
        else:
            try:
                Pilot.create(code=code, first_name=fn, last_name=ln)
                self.form_ln_entry.set('')
                self.form_fn_entry.set('')
                self.form_code_entry.set('')

                self.form.destroy()
                self.clear_tree()
                self.load_data()
                self._root().temporary_status('Added %s %s.' % (fn, ln))
            except:
                messagebox.showinfo(message='The code is already in use!')

