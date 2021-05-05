import os

from Models.CreateDatabase import CreateDatabase
from Utilities import Constants
from Utilities import Logger
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors

logger = Logger.getLogger()


# USE neel;
def use_db_parse(query):
    query = query.replace(";", "")
    words = query.split(' ')
    logger.info('Parsing use DB Query')
    if len(words) == 2:
        if words[0] == "USE":
            if os.path.exists("../" + words[1]):
                logger.info('Trying to change db name')
                Constants.DBNAME = words[1]
                logger.info('DB changed to' + words[1])
                print(f"{Colors.WARNING}Database Changed Successfully.{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}{words[1]} does not exists{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Wrong USE DB Query Syntax{Colors.ENDC}")
            logger.error('Wrong USE DB Query Syntax')
            return None
    else:
        print(f"{Colors.FAIL}Wrong USE DB Query Syntax{Colors.ENDC}")
        logger.error('Wrong USE DB Query Syntax')
        return None
