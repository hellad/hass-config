#!/usr/local/bin/python
# coding: utf8
import json

with open('/config/.shopping_list.json') as data_file:
   shoppingListData = json.load(data_file)

class shoppingList:
    content = u""
    not_complete = 0
    state = u""

myList = shoppingList()

myList.not_complete = 0
myList.state = ""
myList.content = ""

for entry in shoppingListData:
    if not entry['complete']:
        myList.content += u"- %s\n" % entry['name']
        myList.not_complete += 1

if myList.not_complete == 0:
    myList.state = u"Список пуст"
else:
    myList.state = u"Список полон"


print(json.dumps(myList.__dict__))

