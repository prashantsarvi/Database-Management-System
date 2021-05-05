# Syntax : DROP TABLE table_name;

class DropTable:
    def __init__(self, dbname, tablename):
        self.dbname = dbname
        self.tablename = tablename
