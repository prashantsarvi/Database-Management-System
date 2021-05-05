# INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
# I am expecting dictionary for data such as {column1:value1, column2:value2}
class Insert:
    def __init__(self, dbname, tablename, data):
        self.dbname = dbname
        self.tablename = tablename
        self.data = data
