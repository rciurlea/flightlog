import tkinter as tk
from tkinter import ttk, messagebox
from models import Company
from helpers.tree import TreeSorter

class CompaniesFrame(TreeSorter, ttk.Labelframe):
    def __init__(self, parent, *args, **kwargs):
        ttk.Labelframe.__init__(self, parent, *args, **kwargs)
        TreeSorter.__init__(self)

        self.name_var = tk.StringVar()

        self.config(text='Companies')
        self.config(padding=(10, 5, 10, 10))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=('name', ), selectmode='browse')
        self.tree.column('name', width=25, anchor='center')
        self.tree['show'] = 'headings'
        self.tree.heading('name', text='Company Name', command=lambda: self.order('name'))
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        s.grid(row=0, column=1, sticky='ns', pady=(0, 10))
        self.tree['yscrollcommand'] = s.set

        sf = ttk.Frame(self)
        sf.grid(row=1, column=0, columnspan=2, sticky='nsew')
        sf.columnconfigure(0, weight=1)
        sf.columnconfigure(1, weight=1)
        ttk.Button(sf, text="Add Company...", command=self.add_wnd).grid(row=0, column=0, padx=(0,5), sticky='nsew')
        ttk.Button(sf, text="Delete", command=self.remove_comp).grid(row=0, column=1, padx=(5,0), sticky='nsew')

    
    def load_data(self, order_by='name', ascending=True):
        if order_by == 'name':
            if ascending:
                data = Company.select()
            else:
                data = Company.select().order_by(Company.name.desc())

        for c in data:
            self.tree.insert('', 'end', str(c.id), values=(c.name, ))


    def remove_comp(self):
        for i in self.tree.selection():
            guy = Company.get(Company.id == int(i))
            ans = messagebox.askyesno(title='Remove company?', 
                                message='Are you sure you want to remove %s from the database?' % (guy.name, ))
            if ans:
                self.tree.delete(i)
                self._root().temporary_status("Removed %s." % (guy.name, ))
                guy.delete_instance()


    def add_wnd(self):
        root = self._root()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        rh = root.winfo_height()
        w, h = 300, 100
        self.form = tk.Toplevel()
        self.form.title('Add Company')
        self.form.geometry('+%d+%d' % (rx + rw/2 - 100, ry + rh/2 - 100))

        f = ttk.Frame(self.form, padding=(10,10,10,10))
        f.pack()

        ttk.Label(f, text="First Name", anchor="e").grid(row=0, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        fn = ttk.Entry(f, width=10, textvariable=self.name_var)
        fn.grid(row=0, column=1, sticky='nsew', pady=(0,5))
        fn.focus_set()

        f2 = ttk.Frame(f)
        f2.grid(row=3, column=0, columnspan=2, pady=(10,0))
        ttk.Button(f2, text="Save", command=self.save_data).grid(row=0, column=0, padx=(0,5))
        ttk.Button(f2, text="Cancel", command=self.form.destroy).grid(row=0, column=1, padx=(5,0))

        self.form.transient(root)
        self.form.grab_set()
        root.wait_window(self.form)


    def save_data(self):
        name = self.name_var.get().strip()

        if name == '':
            messagebox.showinfo(message="Company name can't be empty!")
        else:
            try:
                Company.create(name=name)
                self.name_var.set('')

                self.form.destroy()
                self.clear_tree()
                self.load_data()
                self._root().temporary_status('Added %s.' % (name, ))
            except:
                messagebox.showinfo(message='Could not add company for some reason!')

