
# from terminaltables import AsciiTable
import json
#
# table_data = [
#     ['Heading1', 'Heading2'],
#     ['row1 column1', 'row1 column2'],
#     ['row2 column1', 'row2 column2'],
#     ['row3 column1', 'row3 column2']
# ]
# table1 = AsciiTable(table_data)
# print(table1.table)

tableJson= open('Details.json')
j=json.load(tableJson)
print(j['columns'])
# list1=[]
# for i in j['columns']:
#     print(i)
#     for j in i:
#         list1.append((j))
#     # for j in i.values():
#     #     list1.append(j)
# print(list1)
# tableJson.close()
