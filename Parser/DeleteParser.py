import re

from Models.DeleteFromTable import DeleteFromTable
from Models.Select import select
from Utilities import Logger, Constants
from Query_Execution_Engine import Engine

logger = Logger.getLogger()


def DeleteParser(userInput):
    try:

        deleteRegex = "DELETE\sFROM\s(\w+)(?:\sWHERE\s(.*))?"

        m = re.match(deleteRegex, userInput, re.IGNORECASE)

        tableName = m[1]
        whereCondition = m[2]
        if whereCondition is not None:

            if '>=' not in whereCondition and '<=' not in whereCondition:
                if '=' in whereCondition:
                    conditionType = 'EQ'
                    whereCondition = whereCondition.replace(" ", "")
                    whereCondition = whereCondition.split("=")
                    whereCondition = {
                        whereCondition[0]: whereCondition[1]
                    }
            if '>' in whereCondition and '=' not in whereCondition:
                conditionType = 'GT'
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split(">")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }
            if '<' in whereCondition and '=' not in whereCondition:
                conditionType = "LT"
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split("<")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }
            if '>=' in whereCondition:
                conditionType = 'GE'
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split(">=")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }

            if '<=' in whereCondition:
                conditionType = 'LE'
                whereCondition = whereCondition.replace(" ", "")
                whereCondition = whereCondition.split("<=")
                whereCondition = {
                    whereCondition[0]: whereCondition[1]
                }
            logger.info('Trying to delete record from Table: ' + str(m[1]) + ' in DB ' + str(Constants.DBNAME))
            return DeleteFromTable(Constants.DBNAME, tableName, whereCondition, conditionType)

        if whereCondition is None:
            logger.info('Trying to delete record from Table: ' + str(m[1]) + ' in DB ' + str(Constants.DBNAME))
            return DeleteFromTable(Constants.DBNAME, tableName)

    except:
        logger.error('Wrong Delete from Table Query Syntax')
        print('Wrong Delete from Table Query Syntax')
        return None


if __name__ == '__main__':
    delete_Object = DeleteParser("delete from Details")
    print(Engine.deletefromtable(delete_Object))
