# Here I am expecting columns in a dictionary form such as {"id":"int", "name":"varchar[20]"}

class Createtable:
    def __init__(self, dbname, tablename, columns, primarykey=None,foreignkey=None,referencetable=None):
        self.dbname = dbname
        self.tablename = tablename
        self.columns = columns
        self.primarykey = primarykey
        self.foreignkey = foreignkey
        self.referencetable = referencetable
