import re

from Models.UpdateTable import UpdateTable
from Models.CreateDatabase import CreateDatabase
from Utilities import Logger, Constants
from Query_Execution_Engine import Engine

logger = Logger.getLogger()


def updateParser(userInput):
    try:
        logger.info('Parsing Update Query')
        updateRegex = "UPDATE\\s(\\w+)\\sSET\\s(.*)\\sWHERE\\s(.*)?"
        setCondition = {}
        m = re.match(updateRegex, userInput, re.IGNORECASE)
        setValues = m[2]
        if setValues is not None:
            setConditionList = setValues.split(",")

            for x in setConditionList:
                xList = x.split("=")

                # print(xList)
                key = xList[0].strip()
                value = xList[1].strip()
                setCondition.update({
                    key: value
                })

        tableName = m[1]
        whereCondition = m[3]
        if whereCondition is not None:
            pass

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

        logger.info('Trying to Update data from Table: ' + str(m[1]) + ' in DB ' + str(Constants.DBNAME))
        return UpdateTable(Constants.DBNAME, tableName, setCondition, whereCondition, conditionType)
    except:
        logger.error('Wrong Update Query Syntax')
        print("Wrong Update Query Syntax")
        return None

    # return("Please enter valid SQL Query")


if __name__ == '__main__':
    updateObject = updateParser("UPDATE Details SET name=Natasha WHERe id=4")
    # print("Condition is:", updateObject.condition)
    # print(Engine.updatetable(updateObject))
