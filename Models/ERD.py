import json
import os

import pyfiglet

from Models.Select import select
from Query_Execution_Engine.Engine import selectfrom, checkcolumnexist
from Utilities import Constants


class ERD:
    def __init__(self, dbname):
        self.dbname = dbname
        self.erd = ""

    def create(self):
        content = ""
        title = pyfiglet.figlet_format("ER - DIAGRAM", font="slant")
        content = content + title
        directorypath = "../" + self.dbname
        listofiles = os.listdir(directorypath)
        if (listofiles == []):
            return "No table exist is the database."
        else:
            with open("../" + self.dbname + "/" + self.dbname + "_DB_Metadata.json", "r+") as file:
                metadata = json.load(file)
                tables = metadata["Tables"]
                for table in tables:
                    content = content + self.fetchtabledata(table)
                    content = content + "\n ------------------------------------------------------------------------------------------------------------------------------------"
            self.savetofile(content)
            return content

    def checkcardinality(self, tablename, tb_pk, refertable, key):
        return_str = "1 to M"
        data_ref, data_table = selectfrom(select(Constants.DBNAME, refertable, [key], None, None)), selectfrom(
            select(Constants.DBNAME, tablename, [key], None, None))

        table_values = ([d[str(key)] for d in data_table])
        if len(set(table_values)) == len(table_values):
            return_str = "1 to 1"
        return return_str

    def fetchtabledata(self, tablename):
        template = {"Table name:": None, "Attributes are:": None}
        with open("../" + self.dbname + "/" + tablename + "_metadata.json", "r+") as file:
            tempstring = ""
            metadata = json.load(file)
            tempstring = ("\n Table name:" + tablename)
            # template["Table name:"] = tablename
            attributelist = []
            for col in metadata["Columns"]:
                attributelist.append(col["name"])
            tempstring = tempstring + "\n Attributes of table are:" + str(attributelist)
            # template["Attributes are:"] = attributelist

            if "primary key" in metadata:
                tempstring = tempstring + "\n The primary key is:" + metadata["primary key"]
            if "foreign key" in metadata:
                tempstring = tempstring + "\n Foreign key of table is:" + metadata[
                    "foreign key"] + " and reference table is:" + metadata["reference table"]
                cardinality = self.checkcardinality(tablename, metadata["primary key"], metadata["reference table"],
                                                    metadata["foreign key"])
                tempstring = tempstring + "\n Cardinality between " + tablename + " table and " + metadata[
                    "reference table"] + " table is : " + cardinality
        return tempstring

    def savetofile(self, content):
        with open("../ERD/" + self.dbname + ".txt", "w+") as file:
            file.write(content)


if __name__ == '__main__':
    erd = ERD("Student")
    print(erd.create())
