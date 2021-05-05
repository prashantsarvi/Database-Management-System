from Models.CreateDatabase import CreateDatabase
from Utilities import Logger
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors

logger = Logger.getLogger()


# CREATE DATABASE neel;
def create_db_parse(query):
    query = query.replace(";", "")
    words = query.split(' ')
    logger.info('Parsing create DB Query')
    if len(words) == 3:
        if words[0] == "CREATE":
            if words[1] == "DATABASE":
                logger.info('Trying to create DB ' + str(words[2]))
                return CreateDatabase(words[2])
            else:
                print(f"{Colors.FAIL}Wrong Create Database Query Syntax{Colors.ENDC}")
                logger.error('Wrong Create Database Query Syntax')
                return None
        else:
            print(f"{Colors.FAIL}Wrong Create Database Query Syntax{Colors.ENDC}")
            logger.error('Wrong Create Database Query Syntax')
            return None
    else:
        print(f"{Colors.FAIL}Wrong Create Database Query Syntax{Colors.ENDC}")
        logger.error('Wrong Create Database Query Syntax')
        return None

