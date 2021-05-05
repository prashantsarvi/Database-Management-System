import re
import Utilities.Constants as constant
from Models.CreateTable import Createtable
import Utilities.Logger as Logger
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors

logger = Logger.getLogger()

# REFERENCES:
# https://stackoverflow.com/questions/62311026/how-to-extract-the-table-name-from-a-create-update-insert-statement-in-an-sql-qu
# https://stackoverflow.com/questions/2785702/use-javascript-regex-to-extract-column-names-from-sqlite-create-table-sql

def create_table(query):
    try:
        logger.info('Parsing create table Query')
        table_name = re.match(
            "(?:(?:CREATE(?:(?:\s*\/\*.*\*\/\s*?)*\s+OR(?:\s*\/\*.*\*\/\s*?)*\s+REPLACE)?|DROP)"
            "(?:\s*\/\*.*\*\/\s*?)*\s+TABLE(?:(?:\s*\/\*.*\*\/\s*?)*\s+IF(?:\s*\/\*.*\*\/\s*?)"
            "*\s+EXISTS)?|UPDATE|DELETE|INSERT(?:\s*\/\*.*\*\/\s*?)*\s+INTO)(?:\s*\/\*.*\*\/\s*?)*\s+([^\s\/*]+)",
            query)
        cols = {}
        PK = None
        FK = None
        RT = None
        parse_cols = re.match("CREATE\s+TABLE\s+(\S+)\s*\((.*)\)", query)[2].split(',')
        for col in parse_cols:
            col = col.strip()
            keyVal = col.split(' ')
            if keyVal[0] == "PRIMARY":
                if keyVal[1] == "KEY":
                    PK = re.match("\(([^)]+)\)", keyVal[2])[1]
                else:
                    print(f"{Colors.FAIL}Wrong Create Table Query Syntax{Colors.ENDC}")

            if keyVal[0] == "FOREIGN":
                if keyVal[1] == "KEY":
                    FK = re.match("\(([^)]+)\)", keyVal[2])[1]
                    if keyVal[3] == "REFERENCES":
                        RT = keyVal[4]
                    else:
                        print(f"{Colors.FAIL}Wrong Create Table Query Syntax{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}Wrong Create Table Query Syntax{Colors.ENDC}")
            else:
                cols[str(keyVal[0])] = str(keyVal[1])
        logger.info("Trying to create Table " + str(table_name[1]) + " in " + str(constant.DBNAME))

        return Createtable(constant.DBNAME, table_name[1], cols, PK, FK, RT)

    except:
        print(f"{Colors.FAIL}Wrong Create Table Query Syntax{Colors.ENDC}")
        logger.error('Wrong Create Table Query')
        return None
    
if __name__ == '__main__':
    create_table('CREATE TABLE Orders (OrderID int, OrderNumber int, PersonID int, PRIMARY KEY (OrderID), FOREIGN KEY (PersonID) REFERENCES Persons (PersonID));')
