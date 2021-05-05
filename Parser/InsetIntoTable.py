import re
import Utilities.Constants as Constants
from Models.Insert import Insert
from Utilities import Logger
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors

logger = Logger.getLogger()


def insert_parse(query):
    try:
        logger.info('Parsing Insert Query')
        data = re.match("INSERT INTO (\S+) \((.*)\) VALUES \((.*)\)", query)
        cols = data[2].split(",")
        values = data[3].replace('\'', "").split(",")

        cols = [x.strip(' ') for x in cols]
        values = [x.strip(' ') for x in values]

        if len(cols) == len(values):
            colValue = dict(zip(cols, values))

        logger.info('Trying to insert data into Table: ' + str(data[1]) + ' in DB ' + str(Constants.DBNAME))
        return Insert(Constants.DBNAME, data[1], colValue)

    except:
        logger.error('Wrong Insert Query Syntax')
        print(f"{Colors.FAIL}Wrong Insert Query Syntax{Colors.ENDC}")
        return None


if __name__ == '__main__':
    insert_object = insert_parse('INSERT INTO Persons (PersonID,LastName,FirstName,Address,City) VALUES (1,dabhi,neel,Quinpool,halifax)')
    # engine = Engine()
    print(Engine.insertdata(insert_object))