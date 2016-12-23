class TreeSorter:
    def __init__(self):
        self.sort_by = ''
        self.prev_sort = ''
        self.ascending = False

    def set_arrow(self, column):
        heading = self.tree.heading(column, 'text')
        if heading[-1] in (u"\u25B4" + u"\u25BE"):
            heading = heading[:-2]
        if self.ascending:
            heading += ' ' + u"\u25BE"
        else:
            heading += ' ' + u"\u25B4"
        self.tree.heading(column, text=heading)

    def remove_arrow(self, column):
        heading = self.tree.heading(column, 'text')
        heading = heading[:-2]
        self.tree.heading(column, text=heading)

    def order(self, field):
        if self.prev_sort != field:
            self.ascending = False
            if self.prev_sort != '':
                self.remove_arrow(self.prev_sort)
        self.sort_by = field
        self.prev_sort = field
        self.ascending = not self.ascending
        self.clear_tree()
        self.load_data(self.sort_by, self.ascending)
        self.set_arrow(field)
        
    def clear_tree(self):
        for child_node in self.tree.get_children():
            self.tree.delete(child_node)
