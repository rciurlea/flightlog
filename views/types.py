import tkinter as tk
from tkinter import ttk, messagebox
from models import ACType, Aircraft
from helpers.tree import TreeSorter

class TypesFrame(TreeSorter, ttk.Labelframe):
    def __init__(self, parent, *args, **kwargs):
        ttk.Labelframe.__init__(self, parent, *args, **kwargs)
        TreeSorter.__init__(self)

        self.name_var = tk.StringVar()
        self.manufacturer_var = tk.StringVar()
        self.me_var = tk.StringVar()
        self.me_var.set('No')
        self.class_var = tk.StringVar()

        self.config(text='Aircraft Types')
        self.config(padding=(10, 5, 10, 10))
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=('name', 'manufacturer', 'multi_engine', 'what_is_it'), selectmode='browse')
        self.tree.column('name', anchor='center', width=30)
        self.tree.column('manufacturer', anchor='center', width=50)
        self.tree.column('multi_engine', anchor='center', width=20)
        self.tree.column('what_is_it', anchor='center', width=50)
        self.tree['show'] = 'headings'
        self.tree.heading('name', text='Type', command=lambda: self.order('name'))
        self.tree.heading('manufacturer', text='Manufacturer', command=lambda: self.order('manufacturer'))
        self.tree.heading('multi_engine', text='M/E', command=lambda: self.order('multi_engine'))
        self.tree.heading('what_is_it', text='Class', command=lambda: self.order('what_is_it'))
        self.tree.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

        s = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        s.grid(row=0, column=1, sticky='ns', pady=(0, 10))
        self.tree['yscrollcommand'] = s.set

        sf = ttk.Frame(self)
        sf.grid(row=1, column=0, columnspan=2, sticky='nsew')
        sf.columnconfigure(0, weight=1)
        sf.columnconfigure(1, weight=1)
        ttk.Button(sf, text="Add Type...", command=self.add_pilot_wnd).grid(row=0, column=0, padx=(0,5), sticky='nsew')
        ttk.Button(sf, text="Delete", command=self.remove_type).grid(row=0, column=1, padx=(5,0), sticky='nsew')

    
    def load_data(self, order_by='name', ascending=True):
        if order_by == 'name':
            if ascending:
                data = ACType.select().order_by(ACType.name)
            else:
                data = ACType.select().order_by(ACType.name.desc())
        elif order_by == 'manufacturer':
            if ascending:
                data = ACType.select().order_by(ACType.manufacturer)
            else:
                data = ACType.select().order_by(ACType.manufacturer.desc())
        elif order_by == 'multi_engine':
            if ascending:
                data = ACType.select().order_by(ACType.multi_engine)
            else:
                data = ACType.select().order_by(ACType.multi_engine.desc())
        else:
            if ascending:
                data = ACType.select().order_by(ACType.what_is_it)
            else:
                data = ACType.select().order_by(ACType.what_is_it.desc())

        for t in data:
            self.tree.insert('', 'end', str(t.id), values=(t.name, t.manufacturer, t.multi_engine, t.what_is_it))


    def remove_type(self):
        for i in self.tree.selection():
            guy = ACType.get(ACType.id == int(i))
            dependent = Aircraft.select().where(Aircraft.actype == guy).count()
            if dependent != 0:
                messagebox.showerror("Not so fast!", "Can't remove %s because there are %d aircraft of that type. Delete those first." % (guy.name, dependent))
                return

            ans = messagebox.askyesno(title='Remove type?', 
                                message='Are you sure you want to remove %s from the database?' % (guy.name,))
            if ans:
                self.tree.delete(i)
                self._root().temporary_status("Removed %s " % (guy.name,))
                guy.delete_instance()


    def add_pilot_wnd(self):
        root = self._root()
        rx = root.winfo_rootx()
        ry = root.winfo_rooty()
        rw = root.winfo_width()
        rh = root.winfo_height()
        w, h = 300, 100
        self.form = tk.Toplevel()
        self.form.title('Add Type')
        self.form.geometry('+%d+%d' % (rx + rw/2 - 100, ry + rh/2 - 100))

        f = ttk.Frame(self.form, padding=(10,10,10,10))
        f.pack()

        ttk.Label(f, text="Name", anchor="e").grid(row=0, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        f_name = ttk.Entry(f, width=10, textvariable=self.name_var)
        f_name.grid(row=0, column=1, sticky='nsew', pady=(0,5))
        f_name.focus_set()

        ttk.Label(f, text='Manufacturer', anchor="e").grid(row=1, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        f_manufacturer = ttk.Entry(f, width=10, textvariable=self.manufacturer_var)
        f_manufacturer.grid(row=1, column=1, sticky='nsew', pady=(0,5))

        ttk.Label(f, text='Multi-engine', anchor="e").grid(row=2, column=0, sticky='nsew', padx=(0,10), pady=(0,5))
        f_me = ttk.Checkbutton(f, variable=self.me_var, onvalue='Yes', offvalue='No')
        f_me.grid(row=2, column=1, sticky='nsew')

        ttk.Label(f, text='Class', anchor='e').grid(row=3, column=0, sticky='nsew', padx=(0,10))
        f_class = ttk.Combobox(f, textvariable=self.class_var, state='readonly')
        f_class['values'] = ('Plane', 'Helicopter', 'Glider', 'Balloon', 'Airship')
        f_class.grid(row=3, column=1, sticky='nsew')

        f2 = ttk.Frame(f)
        f2.grid(row=4, column=0, columnspan=2, pady=(10,0))
        ttk.Button(f2, text="Save", command=self.save_data).grid(row=0, column=0, padx=(0,5))
        ttk.Button(f2, text="Cancel", command=self.form.destroy).grid(row=0, column=1, padx=(5,0))

        self.form.transient(root)
        self.form.grab_set()
        root.wait_window(self.form)


    def save_data(self):
        name = self.name_var.get().strip()
        manufacturer = self.manufacturer_var.get().strip()
        multiengine = self.me_var.get()
        what_is_it = self.class_var.get()

        if name == '' or manufacturer == '' or what_is_it == '':
            messagebox.showinfo(message="Fill in all the fields first!")
        else:
            try:
                ACType.create(name=name, manufacturer=manufacturer, multi_engine=multiengine, what_is_it=what_is_it)
                self.name_var.set('')
                self.manufacturer_var.set('')
                self.me_var.set('No')
                self.class_var.set('')

                self.form.destroy()
                self.clear_tree()
                self.load_data()
                self._root().temporary_status('Added %s.' % (name, ))
            except Exception as e:
                messagebox.showinfo(message='Shit went wrong: %s' % (e, ))

