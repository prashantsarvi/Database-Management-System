#inputQuery = "DELETE FROM TABLE_NAME WHERE COL1=VAL1;"

class DeleteFromTable:
    def __init__(self,dbname,tablename,condition=None,type="EQ"):
        self.dbname = dbname
        self.tablename = tablename
        self.condition = condition
        self.type = type