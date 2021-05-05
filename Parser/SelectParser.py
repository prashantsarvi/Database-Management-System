import re
from Models.CreateDatabase import CreateDatabase
from Models.Select import select
from Utilities import Logger, Constants
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors

logger = Logger.getLogger()


def selectParser(userInput):
    try:
        logger.info('Parsing Select Query')
        selectRegex = "SELECT\s((?:\*)|(?:(?:\w+)(?:,\s?\w+)*))\sFROM\s(\w+)(?:\sWHERE\s(.*))?"
        m = re.match(selectRegex, userInput, re.IGNORECASE)
        records = m[1]

        if '*' in records:
            records = None
        else:
            records = records.replace(" ", "")
            records = records.split(",")

        tableName = m[2]
        whereCondition = m[3]

        if whereCondition is not None:

            if '>=' not in whereCondition and '<=' not in whereCondition:
                if '=' in whereCondition:
                    conditionType = 'EQ'
                    whereCondition = whereCondition.replace(" ", "")
                    whereCondition = whereCondition.split("=")
                    whereCondition = {
                        whereCondition[0]: whereCondition[1]
                    }
            elif '>' in whereCondition and '=' not in whereCondition:
                conditionType = 'GT'
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split(">")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }
            elif '<' in whereCondition and '=' not in whereCondition:
                conditionType = "LT"
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split("<")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }
            elif '>=' in whereCondition:
                conditionType = 'GE'
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split(">=")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }

            elif '<=' in whereCondition:
                conditionType = 'LE'
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split("<=")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }
            else:
                logger.error('Wrong Select Query Syntax')
                return None
            logger.info('Trying to retrieve data from Table: ' + str(m[2]) + ' in DB ' + str(Constants.DBNAME))
            return select(Constants.DBNAME, tableName, records, whereCondition, conditionType)

        if whereCondition is None:
            logger.info('Trying to retrieve data from Table: ' + str(m[2]) + ' in DB ' + str(Constants.DBNAME))
            return select(Constants.DBNAME, tableName, records)
    except:
        logger.error('Wrong Select Query Syntax')
        print(f"{Colors.FAIL}Wrong Select Query Syntax{Colors.ENDC}")
        return None


if __name__ == '__main__':
    selectObject = selectParser("SELECT * FROm Details")
