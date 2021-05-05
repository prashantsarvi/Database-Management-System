# SELECT column1, column2, ... FROM table_name WHERE condition;
# Columns will be list of column and if it is * then no need to pass anything otherwise it will be list of columns
# condition is by default null but if it is then it will be list of condition
# Condition will be dictionary for example contry = "India" then I expect {"contry":"India"}
# Type of condition such as EQ, LT, GT, LE, GE , NE
class select:
    def __init__(self, dbname, tablename, columns=None, condition=None, type="EQ"):
        self.dbname = dbname
        self.tablename = tablename
        self.columns = columns
        self.condition = condition
        self.type = type
