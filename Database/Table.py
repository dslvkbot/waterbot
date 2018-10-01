import Database.Interaction as interact

def list_to_sqlarray(lst, delete_quote = False):
    string = str(lst).replace('[', '').replace(']', '')
    
    if delete_quote:
        string = string.replace("'", '')
    return string
    
class Table:

    def __init__(self, name):
        self.name = name
        self.columns = {}

    def add_column(self, name = None, type = None):

        if type is None:
            assert 0, "Impossible define type column"
        if name is None:
            assert 0, "Impossible define name column"

        self.columns.update({name: type})

        query = "ALTER TABLE {table_name} ADD {column_name} {column_type}".format(table_name=self.name, column_name=name, column_type=type)
        return interact.execute(query)

    def clear_table(self):
        interact.execute("DELETE TABLE {name}".format(name=self.name))

    def get_info_by_user_id(self, user_id):
        query = "SELECT * FROM {table} WHERE user_id like '{user_id}'".format(table=self.name, user_id=user_id)
        print(query)
        return interact.execute(query)

    def get_info_by_time(self, time):
        query = "SELECT * FROM {table} WHERE time like '{time}'".format(table=self.name, time=time)
        print(query)
        return interact.execute(query)

    def create_table(self, columns):
        interact.execute("CREATE TABLE {name} (CREATE_TABLE text)".format(name=self.name))
        self.columns = columns
        for name in columns:
            type = columns[name]
            if type is None:
                continue
            self.add_column(name, type)

    def insert_into(self, fields):
        names = list()
        values = list()
        for name in fields.keys():
            value = fields[name]
            if value is None:
                continue
            names.append(name)
            values.append(value)

        query = "INSERT INTO {table_name} ({names}) VALUES({values})".format(table_name=self.name, names=list_to_sqlarray(names, True), values=list_to_sqlarray(values))
        print(query)
        return interact.execute(query)

    def select(self, names):
        query = "SELECT {names} FROM {table}".format(names = list_to_sqlarray(names, True), table = self.name)
        return interact.execute(query)
