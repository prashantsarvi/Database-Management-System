import json
import os.path
from Models.CreateTable import Createtable
from Utilities import Constants
from Utilities import Logger
from Utilities.Colors import Colors

logger = Logger.getLogger()

def createdatabase(createobject):
    if os.path.exists('../' + createobject.dbname):
        logger.info("Database " + createobject.dbname + " already exists.")
        return (f"{Colors.FAIL}Database already exist.{Colors.ENDC}")

    else:
        os.makedirs("../" + createobject.dbname)
        logger.info("Database " + createobject.dbname + " created successfully.")
        return (f"{Colors.OKGREEN}Database Created.{Colors.ENDC}")

def createtable(insert_entry):
    if insert_entry != None:
        if os.path.exists('../' + insert_entry.dbname + '/' + insert_entry.tablename + '_metadata.json'):
            return (f"{Colors.FAIL}Table already exist.{Colors.ENDC}")

        json_object = {}
        column_json = []
        key_list = insert_entry.columns.keys()
        value_list = insert_entry.columns.values()
        for key, value in insert_entry.columns.items():
            column_dict = {}
            column_dict["name"] = key
            column_dict["type"] = value
            column_json.append(column_dict)

        json_object["Columns"] = column_json
        json_object["primary key"] = insert_entry.primarykey

        if(insert_entry.foreignkey != None):
            if(os.path.exists("../"+insert_entry.dbname+"/"+insert_entry.referencetable+"_metadata.json")):
                reference_metadata = json.load(open("../"+insert_entry.dbname+"/"+insert_entry.referencetable+"_metadata.json","r"))
                if(reference_metadata["primary key"] == insert_entry.foreignkey):
                    json_object["foreign key"] = insert_entry.foreignkey
                    json_object["reference table"] = insert_entry.referencetable
                else:
                    return("The key you want to refer is not a primary key of reference table.")
            else:
                return ("Reference table for foreign key does not exist in the database")

        with open("../" + insert_entry.dbname + "/" + insert_entry.dbname + "_DB_Metadata.json", 'r') as tempfile:
            data1 = json.load(tempfile)
            current_list = data1["Tables"]
        with open("../" + insert_entry.dbname + "/" + insert_entry.dbname + "_DB_Metadata.json", 'w') as writefile:
            current_list.append(insert_entry.tablename)
            data1["Tables"] = current_list
            writefile.seek(0)
            json.dump(data1, writefile)
            writefile.truncate()
            # json.dump(data1,tempfile)
        with open("../" + insert_entry.dbname + '/' + insert_entry.tablename + '_metadata.json', 'w') as metadatafile:
            json.dump(json_object, metadatafile)
        init = {"columns": []}
        with open('../' + insert_entry.dbname + '/' + insert_entry.tablename + '.json', "w") as datafile:
            json.dump(init, datafile)

        logger.info(insert_entry.tablename + " table created successfully.")
        return (f"{Colors.OKGREEN}Table created successfully.{Colors.ENDC}")

    else:
        logger.error("error occured during creating table named " + insert_entry.tablename)
        return (f"{Colors.FAIL}Error in creating table.{Colors.ENDC}")

def insertdata(InsertObject, transactionobject=None):
    if (checklockontable(InsertObject.dbname, InsertObject.tablename, Constants.CURRENT_USER) == None):
        if os.path.exists("../" + InsertObject.dbname + "/" + InsertObject.tablename + ".json"):
            with open("../" + InsertObject.dbname + "/" + InsertObject.tablename + "_metadata.json",
                      "r+") as metadatafile:
                metadata = json.load(metadatafile)
                listofcolumns = []
                for x in metadata['Columns']:
                    listofcolumns.append(x['name'])
                if (set(listofcolumns) == set(InsertObject.data.keys())):
                    pass
                else:
                    return (f"{Colors.FAIL}Please enter valid columns.{Colors.ENDC}")

            if (checkduplicate(InsertObject.dbname, InsertObject.tablename, InsertObject.data)):
                logger.error("Primary key Constraint: Data with primary key already exist in table.")
                return (
                    f"{Colors.FAIL}Primary key Constraint: Data with primary key already exist in table.{Colors.ENDC}")
            with open("../" + InsertObject.dbname + "/" + InsertObject.tablename + ".json", "r+") as jsonfile:
                data = json.load(jsonfile)
                current_list = data["columns"]

                for key, value in InsertObject.data.items():
                    if (checkcolumnexist(InsertObject.dbname, InsertObject.tablename, key) == False):
                        logger.error("Insert Failed: The column you are trying to insert does not exist in the table.")
                        return (
                            f"{Colors.FAIL}Insert Failed: The column you are trying to insert does not exist in the table.{Colors.ENDC}")

                current_list.append(InsertObject.data)
                data["columns"] = current_list

                # This code will save data into table.
                if (transactionobject == None):
                    save(InsertObject.dbname, InsertObject.tablename, data)
                else:
                    tempdict = {InsertObject.tablename: data}
                    # print("Temp dict", tempdict)
                    transactionobject.listofdata.append(tempdict)
                    transactionobject.createlockontable(InsertObject.tablename, "Exclusive")
                # jsonfile.seek(0)
                # json.dump(data, jsonfile)
                logger.info("Data inserted in the " + InsertObject.tablename + " successfully.")
                return (f"{Colors.OKGREEN}Data inserted successfully.{Colors.ENDC}")

        else:
            logger.error("error occured during inserting data into the table " + InsertObject.tablename)
            return (f"{Colors.FAIL}Insert Failed. ERROR: Table does not exist.{Colors.ENDC}")
    else:
        return (
            f"{Colors.FAIL}Sorry you can not perform any operation because another user has already acquired lock on this table.{Colors.ENDC}")

def selectfrom(selectObject, transactionobject=None):
    if ((checklockontable(selectObject.dbname, selectObject.tablename, Constants.CURRENT_USER) == None) or
            (checklockontable(selectObject.dbname, selectObject.tablename, Constants.CURRENT_USER) == "Shared")):
        if os.path.exists("../" + selectObject.dbname + "/" + selectObject.tablename + ".json"):
            with open("../" + selectObject.dbname + "/" + selectObject.tablename + ".json", "r+") as jsonfile:

                if transactionobject != None:
                    transactionobject.createlockontable(selectObject.tablename, "Shared")
                data = json.load(jsonfile)
                filtered_data = []
                current_data = data["columns"]

                if (selectObject.condition == None):
                    filtered_data = current_data
                else:

                    # print(current_data)
                    for key, value in selectObject.condition.items():
                        left = key
                        right = value
                    if (checkcolumnexist(selectObject.dbname, selectObject.tablename, left) == False):
                        logger.error(
                            "ERROR: The column specified in the condition does not exist in the " + selectObject.tablename + " table.")
                        return (
                            f"{Colors.FAIL}The column specified in the condition does not exist in the {selectObject.tablename} table.{Colors.ENDC}")

                    for row in current_data:
                        if (selectObject.type == "EQ"):
                            if (row[left] == right):
                                filtered_data.append(row)
                        elif (selectObject.type == "LT"):
                            if (row[left] < right):
                                filtered_data.append(row)
                        elif (selectObject.type == "LE"):
                            if (row[left] <= right):
                                filtered_data.append(row)
                        elif (selectObject.type == "GT"):
                            if (row[left] > right):
                                filtered_data.append(row)
                        elif (selectObject.type == "GE"):
                            if (row[left] >= right):
                                filtered_data.append(row)
                        elif (selectObject.type == "NE"):
                            if (row[left] != right):
                                filtered_data.append(row)

                if selectObject.columns == None:
                    logger.info("Select operation performed on table named " + selectObject.tablename)
                    return filtered_data
                else:
                    for col in selectObject.columns:
                        if (checkcolumnexist(selectObject.dbname, selectObject.tablename, col) == False):
                            logger.error(
                                "The column specified in the selection does not exist in the" + selectObject.tablename + " table.")
                            return (
                                f"{Colors.FAIL}The column specified in the selection does not exist in the {selectObject.tablename} table.{Colors.ENDC}")

                    outputlist = []
                    # print("Filter:", filtered_data)
                    for row in filtered_data:
                        newdict = {k: row[k] for k in selectObject.columns}
                        outputlist.append(newdict)
                    return outputlist
        else:
            logger.error("Select operation failed.")
            return (f"{Colors.FAIL}Select Failed. Table does not exist.{Colors.ENDC}")

    else:
        return (
            f"{Colors.FAIL}Sorry you can not perform any operation because another user has already acquired lock on this table.{Colors.ENDC}")

def updatetable(UpdateObject, transactionobject=None):
    if ((checklockontable(UpdateObject.dbname, UpdateObject.tablename, Constants.CURRENT_USER) == None)):

        if os.path.exists("../" + UpdateObject.dbname + "/" + UpdateObject.tablename + ".json"):
            with open("../" + UpdateObject.dbname + "/" + UpdateObject.tablename + ".json", "r+") as jsonfile:
                data = json.load(jsonfile)
                filtered_data = []
                current_data = data["columns"]

                for key, value in UpdateObject.condition.items():
                    left = key
                    right = value
                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename, left) == False):
                    logger.error(
                        "ERROR: The column specified in the condition does not exist in the " + UpdateObject.tablename + " table.")
                    return (
                        f"{Colors.FAIL}The column specified in the condition does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")

                with open("../" + UpdateObject.dbname + "/" + UpdateObject.tablename + "_metadata.json",
                          "r+") as metadatafile:
                    metadata = json.load(metadatafile)
                    primarykey = metadata["primary key"]
                templist = []
                for key, value in UpdateObject.columns.items():
                    templist.append(key)
                if (primarykey in templist):
                    return (f"{Colors.FAIL}UPDATE CONSTRAINT: You can not update value of primary key.{Colors.ENDC}")
                for row in current_data:
                    if (UpdateObject.type == "EQ"):
                        if (row[left] == right):
                            for key, value in UpdateObject.columns.items():
                                column_name = key
                                column_value = value
                                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename,
                                                     column_name) == False):
                                    logger.error(
                                        "ERROR: The column you want to update " + column_name + " does not exist in the " + UpdateObject.tablename + " table")
                                    return (
                                        f"{Colors.FAIL}The column you want to update {column_name} does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")
                                row[column_name] = column_value
                            filtered_data.append(row)
                        else:
                            filtered_data.append(row)
                    elif (UpdateObject.type == "LT"):
                        if (row[left] < right):
                            for key, value in UpdateObject.columns.items():
                                column_name = key
                                column_value = value
                                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename,
                                                     column_name) == False):
                                    logger.error(
                                        "ERROR: The column you want to update " + column_name + " does not exist in the " + UpdateObject.tablename + " table")
                                    return (
                                        f"{Colors.FAIL}The column you want to update {column_name} does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")
                                row[column_name] = column_value
                            filtered_data.append(row)
                        else:
                            filtered_data.append(row)

                    elif (UpdateObject.type == "LE"):
                        if (row[left] <= right):
                            for key, value in UpdateObject.columns.items():
                                column_name = key
                                column_value = value
                                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename,
                                                     column_name) == False):
                                    logger.error(
                                        "ERROR: The column you want to update " + column_name + " does not exist in the " + UpdateObject.tablename + " table")
                                    return (
                                        f"{Colors.FAIL}The column you want to update {column_name} does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")

                                row[column_name] = column_value
                            filtered_data.append(row)
                        else:
                            filtered_data.append(row)

                    elif (UpdateObject.type == "GT"):
                        if (row[left] > right):
                            for key, value in UpdateObject.columns.items():
                                column_name = key
                                column_value = value
                                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename,
                                                     column_name) == False):
                                    logger.error(
                                        "ERROR: The column you want to update " + column_name + " does not exist in the " + UpdateObject.tablename + " table")
                                    return (
                                        f"{Colors.FAIL}The column you want to update {column_name} does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")

                                row[column_name] = column_value
                            filtered_data.append(row)
                        else:
                            filtered_data.append(row)

                    elif (UpdateObject.type == "GE"):
                        if (row[left] >= right):
                            for key, value in UpdateObject.columns.items():
                                column_name = key
                                column_value = value
                                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename,
                                                     column_name) == False):
                                    logger.error(
                                        "ERROR: The column you want to update " + column_name + " does not exist in the " + UpdateObject.tablename + " table")
                                    return (
                                        f"{Colors.FAIL}The column you want to update {column_name} does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")

                                row[column_name] = column_value
                            filtered_data.append(row)
                        else:
                            filtered_data.append(row)

                    elif (UpdateObject.type == "NE"):
                        if (row[left] != right):
                            for key, value in UpdateObject.columns.items():
                                column_name = key
                                column_value = value
                                if (checkcolumnexist(UpdateObject.dbname, UpdateObject.tablename,
                                                     column_name) == False):
                                    logger.error(
                                        "ERROR: The column you want to update " + column_name + " does not exist in the " + UpdateObject.tablename + " table")
                                    return (
                                        f"{Colors.FAIL}The column you want to update {column_name} does not exist in the {UpdateObject.tablename} table.{Colors.ENDC}")

                                row[column_name] = column_value
                            filtered_data.append(row)
                        else:
                            filtered_data.append(row)
            with open("../" + UpdateObject.dbname + "/" + UpdateObject.tablename + ".json", "r+") as jsonfile:
                filedata = json.load(jsonfile)
                filedata["columns"] = filtered_data

                # This line will save data into persistant form
                if (transactionobject == None):
                    save(UpdateObject.dbname, UpdateObject.tablename, filedata)
                else:
                    tempdict = {UpdateObject.tablename: filedata}
                    transactionobject.listofdata.append(tempdict)
                    transactionobject.createlockontable(UpdateObject.tablename, "Exclusive")

                # jsonfile.seek(0)
                # json.dump(filedata, jsonfile)
                # jsonfile.truncate()
                logger.info("Data updated successfully in the table named " + UpdateObject.tablename)
                return (f"{Colors.OKGREEN}Data updated successfully.{Colors.ENDC}")

        else:
            logger.error("Table does not exist for update named " + UpdateObject.tablename)
            return (f"{Colors.FAIL}Table does not exist.{Colors.ENDC}")

    else:
        return (
            f"{Colors.FAIL}Sorry you can not perform any operation because another user has already acquired lock on this table.{Colors.ENDC}")

# This method will check that database exist or not
def checkdatabaseexist(dbname):
    if os.path.exists('../' + dbname):
        return True
    else:
        return False

def deletefromtable(DeleteObject, transactionobject=None):
    if ((checklockontable(DeleteObject.dbname, DeleteObject.tablename, Constants.CURRENT_USER) == None)):

        if os.path.exists("../" + DeleteObject.dbname + "/" + DeleteObject.tablename + ".json"):
            with open("../" + DeleteObject.dbname + "/" + DeleteObject.tablename + ".json", "r+") as jsonfile:
                data = json.load(jsonfile)
                filtered_data = []
                current_data = data["columns"]

                for key, value in DeleteObject.condition.items():
                    left = key
                    right = value
                if (checkcolumnexist(DeleteObject.dbname, DeleteObject.tablename, left) == False):
                    logger.error(
                        "ERROR: The column specified in the condition does not exist in the " + + " ")
                    return (
                        f"{Colors.FAIL}The column specified in the condition does not exist in the {DeleteObject.tablename} table.{Colors.ENDC}")
                if (DeleteObject.condition != None):
                    for row in current_data:
                        if (DeleteObject.type == "EQ"):
                            if (row[left] != right):
                                filtered_data.append(row)
                            else:
                                pass
                        elif (DeleteObject.type == "LT"):
                            if (row[left] < right):
                                pass
                            else:
                                filtered_data.append(row)

                        elif (DeleteObject.type == "LE"):
                            if (row[left] <= right):
                                pass
                            else:
                                filtered_data.append(row)

                        elif (DeleteObject.type == "GT"):
                            if (row[left] > right):
                                pass
                            else:
                                filtered_data.append(row)

                        elif (DeleteObject.type == "GE"):
                            if (row[left] >= right):
                                pass
                            else:
                                filtered_data.append(row)
                                filtered_data.append(row)
                else:
                    filtered_data = []
                with open("../" + DeleteObject.dbname + "/" + DeleteObject.tablename + ".json", "r+") as jsonfile:
                    filedata = json.load(jsonfile)
                    filedata["columns"] = filtered_data

                    # This line will save data into persistant form
                    if (transactionobject == None):
                        save(DeleteObject.dbname, DeleteObject.tablename, filedata)
                    else:
                        tempdict = {DeleteObject.tablename: filedata}
                        transactionobject.listofdata.append(tempdict)
                        transactionobject.createlockontable(DeleteObject.tablename, "Exclusive")
                    # jsonfile.seek(0)
                    # json.dump(filedata, jsonfile)
                    # jsonfile.truncate()
                    logger.info("Data Deleted successfully in the table named " + DeleteObject.tablename)
                    return (f"{Colors.OKGREEN}Data Deleted successfully.{Colors.ENDC}")


        else:
            logger.error("Table does not exist for delete operation.")
            return (f"{Colors.FAIL}Table does not exist.{Colors.ENDC}")


    else:
        return (
            f"{Colors.FAIL}Sorry you can not perform any operation because another user has already acquired lock on this table.{Colors.ENDC}")

def droptable(DropObject):
    if ((checklockontable(DropObject.dbname, DropObject.tablename, Constants.CURRENT_USER) == None)):
        if os.path.exists("../" + DropObject.dbname + "/" + DropObject.tablename + ".json"):
            os.remove("../" + DropObject.dbname + "/" + DropObject.tablename + ".json")
            os.remove("../" + DropObject.dbname + "/" + DropObject.tablename + "_metadata.json")
            logger.info("Table named " + DropObject.tablename + " created successfully.")
            return (f"{Colors.OKGREEN}Table deleted successfully.{Colors.ENDC}")

        else:
            logger.error("error occured during droping table named " + DropObject.tablename)
            return (f"{Colors.FAIL}Table does not exist.{Colors.ENDC}")

    else:
        return (
            f"{Colors.FAIL}Sorry you can not perform any operation because another user has already acquired lock on this table.{Colors.ENDC}")

# This method will truncate table data
def truncatetable(DropObject):
    if ((checklockontable(DropObject.dbname, DropObject.tablename, Constants.CURRENT_USER) == None)):

        if os.path.exists("../" + DropObject.dbname + "/" + DropObject.tablename + ".json"):
            os.remove("../" + DropObject.dbname + "/" + DropObject.tablename + ".json")
            init = {"columns": []}
            with open("../" + DropObject.dbname + "/" + DropObject.tablename + ".json", "w") as datafile:
                temp = json.dumps(init)
                datafile.write(temp)
            logger.info("Table " + DropObject.tablename + " truncated successfully.")
            return (f"{Colors.OKGREEN}Table data truncated.{Colors.ENDC}")

        else:
            logger.error("error occured during truncating table " + DropObject.tablename)
            return (f"{Colors.FAIL}Table does not exist.{Colors.ENDC}")

    else:
        return (
            f"{Colors.FAIL}Sorry you can not perform any operation because another user has already acquired lock on this table.{Colors.ENDC}")

def save(dbname, tablename, tabledata):
    with open("../" + dbname + "/" + tablename + ".json", "r+") as jsonfile:
        jsonfile.seek(0)
        json.dump(tabledata, jsonfile)
        jsonfile.truncate()

# This function will check that the specific column is there in the table or not.
# This function requires database name, table name and column name
def checkcolumnexist(dbname, tablename, columnname):
    if os.path.exists("../" + dbname + "/" + tablename + "_metadata.json"):
        with open("../" + dbname + "/" + tablename + "_metadata.json", "r") as jsonfile:
            data = json.load(jsonfile)
            listofcolumns = data["Columns"]
            for dict in listofcolumns:
                if (dict["name"] == columnname):
                    return True
            return False
    else:
        return False

def checkduplicate(dbname, tablename, data):
    with open("../" + dbname + "/" + tablename + "_metadata.json", "r+") as metadatafile:
        metadata = json.load(metadatafile)

        primarykey = metadata["primary key"]
    templist = []
    with open("../" + dbname + "/" + tablename + ".json", "r+") as datafile:
        tabledata = json.load(datafile)
        current_list = tabledata["columns"]
    for x in current_list:
        templist.append(x[primarykey])
    if (data[primarykey] in templist):
        return True
    else:
        return False
    pass

def checklockontable(dbname, tablename, user):
    directorypath = "../Transactions"
    listofiles = os.listdir(directorypath);
    if (listofiles == []):
        return None
    else:
        # print(listofiles)
        for file in listofiles:
            if (user + ".json" == file):
                return None
            with open("../Transactions/" + file) as jsonfile:
                transactionobject = json.load(jsonfile)
                if (dbname == transactionobject["dbname"]):
                    for table in transactionobject["tables"]:
                        for key, value in table.items():
                            table_name = key
                            locktype = value
                        if (table_name == tablename):
                            return locktype
        return None

if __name__ == '__main__':
    dict={"id":"int","name":"vatchar"}
    createobject = Createtable("Student","hh",dict,"id","AGENT_CODE","AGENTS")
    print(createtable(createobject))