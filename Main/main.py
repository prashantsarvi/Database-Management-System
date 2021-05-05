import os
import sys

import tabulate
import Utilities.Constants as constant
from Models.ERD import ERD
from Models.Transaction import Transactions
from Parser.CreateDatabase import create_db_parse
from Parser.CreateTable import create_table
from Parser.DeleteParser import DeleteParser
from Parser.DeleteTable import drop_table_parse
from Parser.InsetIntoTable import insert_parse
from Parser.SelectParser import selectParser
from Parser.UpdateParser import updateParser
from Parser.UseDB import use_db_parse
from Query_Execution_Engine import Engine
from Utilities.Colors import Colors
import pyfiglet
from Models import DataDictionary
import getpass


def auth():
    while constant.CURRENT_USER == None:
        user_name = input("Enter username:")
        if user_name == 'root':
            password = input("Enter password:")
            if password == 'root':
                constant.CURRENT_USER = user_name
                return True
            else:
                print(f"{Colors.FAIL}Wrong Password!{Colors.ENDC}")
        elif user_name == 'admin':
            password = input("Enter password:")
            if password == 'admin':
                constant.CURRENT_USER = user_name
                return True
            else:
                print(f"{Colors.FAIL}Wrong Password!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}No such user Exists!{Colors.ENDC}")
    return False


def set_db():
    while constant.DBNAME == None:
        db = input("Enter DB Name:")
        if os.path.exists("../" + db):
            print(f"{Colors.WARNING}Database selected successfully.{Colors.ENDC}")
            constant.DBNAME = db
        else:
            print(f"{Colors.FAIL}{db} does not exists{Colors.ENDC}")


def dict_to_table(dict):
    if type(dict) == str:
        print(f"{Colors.FAIL}{dict}{Colors.ENDC}")
    else:
        if (len(dict) == 0):
            print(f"{Colors.FAIL}No records found{Colors.ENDC}")
        else:
            header = dict[0].keys()
            rows = [x.values() for x in dict]
            print(f"{Colors.WARNING}{tabulate.tabulate(rows, header)}{Colors.ENDC}")


def write_dump(query):
    with open("../querydump.txt", "a+") as myfile:
        myfile.write(query + '\n')

def query_processing():
    Trasections = False

    while True:
        query = input(f"(user-{constant.CURRENT_USER}) Enter a SQL Query ({constant.DBNAME}):")
        if Trasections:

            if 'SELECT' in query:
                parsed = selectParser(query)
                if parsed is not None:
                    dict_to_table(Engine.selectfrom(parsed, obj))

            elif 'CREATE TABLE' in query:
                parsed = create_table(query)
                if parsed is not None:
                    write_dump(query)
                    print(Engine.createtable(parsed, obj))

            elif 'CREATE DATABASE' in query:
                parsed = create_db_parse(query)
                if parsed is not None:
                    write_dump(query)
                    print(Engine.createdatabase(parsed, obj))

            elif 'DELETE FROM' in query:
                parsed = DeleteParser(query)
                if parsed is not None:
                    print(Engine.deletefromtable(parsed, obj))

            elif 'DROP TABLE' in query:
                parsed = drop_table_parse(query)
                if parsed is not None:
                    write_dump(query)
                    print(Engine.droptable(parsed, obj))

            elif 'INSERT INTO' in query:
                parsed = insert_parse(query)
                if parsed is not None:
                    print(Engine.insertdata(parsed, obj))

            elif 'UPDATE' in query:
                parsed = updateParser(query)
                if parsed is not None:
                    print(Engine.updatetable(parsed, obj))

            elif 'USE' in query:
                print(f"{Colors.WARNING}Changing DB is not allowed in transaction.{Colors.ENDC}")

            elif 'COMMIT TRANSACTION' in query:
                Trasections = False
                print(obj.commit())

            elif 'ROLLBACK TRANSACTION' in query:
                Trasections = False
                print(obj.rollback())

            elif "GENERATE ERD" in query:
                erd = ERD(constant.DBNAME)
                print(erd.create())

            elif "QUIT" in query:
                sys.exit("Application Stopped")

            else:
                print(f"{Colors.FAIL}{query} is not a SQL Query.{Colors.ENDC}")

        else:

            if 'SELECT' in query:
                parsed = selectParser(query)
                if parsed is not None:
                    dict_to_table(Engine.selectfrom(parsed))

            elif 'CREATE TABLE' in query:
                parsed = create_table(query)
                if parsed is not None:
                    write_dump(query)
                    print(Engine.createtable(parsed))

            elif 'CREATE DATABASE' in query:
                parsed = create_db_parse(query)
                if parsed is not None:
                    write_dump(query)
                    print(Engine.createdatabase(parsed))

            elif 'DELETE FROM' in query:
                parsed = DeleteParser(query)
                if parsed is not None:
                    print(Engine.deletefromtable(parsed))

            elif 'DROP TABLE' in query:
                parsed = drop_table_parse(query)
                if parsed is not None:
                    write_dump(query)
                    print(Engine.droptable(parsed))

            elif 'INSERT INTO' in query:
                parsed = insert_parse(query)
                if parsed is not None:
                    print(Engine.insertdata(parsed))

            elif 'UPDATE' in query:
                parsed = updateParser(query)
                if parsed is not None:
                    print(Engine.updatetable(parsed))

            elif 'USE' in query:
                parsed = use_db_parse(query)

            elif 'BEGIN TRANSACTION' in query:
                obj = Transactions(constant.CURRENT_USER, constant.DBNAME)
                print(obj.createjsonfile())
                Trasections = True

            elif "GENERATE DATA DICTIONARY" in query:
                print(f"{Colors.OKGREEN}Data Dictionary generated.{Colors.ENDC}")
                DataDictionary.dict_to_table(DataDictionary.DataDictionary(constant.DBNAME))

            elif "GENERATE ERD" in query:
                erd = ERD(constant.DBNAME)
                print(erd.create())

            elif "QUIT" in query:
                sys.exit("Application Stopped")
            else:
                print(f"{Colors.FAIL}{query} is not a SQL Query.{Colors.ENDC}")


if __name__ == '__main__':
    result = pyfiglet.figlet_format("G 4 - D B M S", font="slant")
    print(f"{Colors.OKBLUE}{result}{Colors.ENDC}")
    auth()
    set_db()
    query_processing()
