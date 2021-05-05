import json
from Main import main
from Utilities.Colors import Colors
import tabulate


def dict_to_table(dict):
    if type(dict) == str:
        print(f"{Colors.FAIL}{dict}{Colors.ENDC}")
    else:
        if (len(dict) == 0):
            print(f"{Colors.FAIL}No records found{Colors.ENDC}")
        else:
            header = ["TableName","primary key","Columns (Datatype)"]
            # rows = [x.values() for x in dict]
            rows=[]
            for row in dict:
                templist =[]
                templist.append(row["TableName"])
                templist.append(row["primary key"])
                collist = []
                for col in row["Columns"]:
                    tempstr = str( col["name"] +"("+ col["type"] + ")")
                    collist.append(tempstr)
                templist.append(collist)
                rows.append(templist)
            print(f"{Colors.WARNING}{tabulate.tabulate(rows, header)}{Colors.ENDC}")

def DataDictionary(DBname):
    dictList = []
    import glob, os
    os.chdir("../" + DBname)
    for file in glob.glob("*.json"):
        if "_metadata" in file:
            with open(file, 'r') as metadatafile:
                data = json.load(metadatafile)
                data["TableName"] = file.replace("_metadata.json", "")
                dictList.append(data)
    with open("../" + DBname + '/' + 'DataDictionary.json', 'w') as fout:
        json.dump(dictList, fout)
    return dictList

if __name__ == '__main__':
    dict_to_table(DataDictionary("Student"))