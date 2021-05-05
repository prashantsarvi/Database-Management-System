import os
import json
from Query_Execution_Engine import Engine
from Parser import UpdateParser
from Utilities import Constants
from Utilities.Colors import Colors
from Utilities import Logger

logger = Logger.getLogger()

class Transactions:
    def __init__(self, user, dbname, listofdata=[], tables=[]):
        self.user = user
        self.dbname = dbname
        self.listofdata = listofdata
        self.tables = tables

    def createjsonfile(self):
        if os.path.exists('../Transactions' + '/' + self.user + '.json'):
            logger.warn("Transactions for this user named"+self.user+" is already running.")
            return (f"{Colors.WARNING} Transactions for this user is already running.{Colors.ENDC}")
        else:
            with open('../Transactions/' + Constants.CURRENT_USER + '.json', "w+") as datafile:
                json.dump(self.__dict__, datafile)
            logger.info("Transactions for this user named"+self.user+" has initiated.")
            return (f"{Colors.OKGREEN} Transactions Initiated.{Colors.ENDC}")

    def createlockontable(self, tablename, locktype):
        flag = False
        listoftables = self.tables
        for entry in listoftables:
            if tablename in entry:
                entry[tablename] = locktype
                flag = True
        if flag == False:
            listoftables.append({tablename: locktype})
        self.savetojsonfile()

    def savetojsonfile(self):
        with open('../Transactions' + '/' + self.user + '.json', "w") as datafile:
            json.dump(self.__dict__, datafile)

    def commit(self):
        for data in self.listofdata:
            for key, value in data.items():
                tablename = key
                tabledata = value
        Engine.save(self.dbname, tablename, tabledata)
        os.remove("../Transactions/" + self.user + ".json")
        logger.info("Transaction for the user "+self.user+" committed.")
        return(f"{Colors.OKGREEN} Transactions Committed Successfully.{Colors.ENDC}")


    def rollback(self):
        logger.info("Transaction for the user "+self.user+" rollbacked.")
        os.remove("../Transactions/" + self.user + ".json")
        return(f"{Colors.OKGREEN} Transactions Rollbacked Successfully.{Colors.ENDC}")


if __name__ == '__main__':
    # Steps to deserialize object into file
    with open("../Transactions/" + "root" + ".json") as jsonfile:
        filedata = json.load(jsonfile)

    json_str = json.dumps(filedata)
    resultDict = json.loads(json_str)
    obj = Transactions(**resultDict)

    obj.rollback()
