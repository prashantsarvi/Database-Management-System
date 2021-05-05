# UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;
# columns will be list of value to be updated for example UPDATE Customers SET ContactName = 'Alfred Schmidt', City= 'Frankfurt' WHERE CustomerID = 1;
# for this columns will be = [{"contactname":"Alfred Schmidt"} , {"City":"Frankfurt"}]
# Type of condition such as EQ, LT, GT, LE, GE , NE
# UPDATE Student set name="Dhruvil" WHERE id= "1";

class UpdateTable:
    def __init__(self, dbname, tablename, columns, condition=None, type="EQ"):
        self.dbname = dbname
        self.tablename = tablename
        self.columns = columns
        self.condition = condition
        self.type = type
