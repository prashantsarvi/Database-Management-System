from Models.DropTable import DropTable
import Utilities.Constants as Constants
from Utilities import Logger
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors

logger = Logger.getLogger()


# DROP TABLE table_name;


def drop_table_parse(query):
    try:
        query = query.replace(";", "")
        words = query.split(' ')
        logger.info('Parsing Drop Table Query')
        if len(words) == 3:
            if words[0] == "DROP":
                if words[1] == "TABLE":
                    logger.info('Trying to drop Table ' + str(words[2]))
                    return DropTable(Constants.DBNAME, words[2])
                else:
                    print(f"{Colors.FAIL}Wrong Drop Table Query Syntax{Colors.ENDC}")
                    logger.error('Wrong Drop Table Query Syntax')
                    return None
            else:
                print(f"{Colors.FAIL}Wrong Drop Table Query Syntax{Colors.ENDC}")
                logger.error('Wrong Drop Table Query Syntax')
                return None
        else:
            print(f"{Colors.FAIL}Wrong Drop Table Query Syntax{Colors.ENDC}")
            logger.error('Wrong Drop Table Query Syntax')
            return None
    except:
        print(f"{Colors.FAIL}Wrong Drop Table Query Syntax{Colors.ENDC}")
        logger.error('Wrong Drop Table Query Syntax')
        return None

if __name__ == '__main__':
    print(Engine.droptable(drop_table_parse("DROP TABLE Persons;")))