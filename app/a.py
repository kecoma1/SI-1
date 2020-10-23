import json
import os
import sys

with open('catalogue/catalogue.json', 'r') as myfile:
    data=myfile.read()

# parse file
catalogue = json.loads(data)

print(catalogue['peliculas'][0])

dir_path = homedir = os.path.expanduser("~")
dir_path += "/public_html/usuarios"
print(dir_path)

card = "a a a aa a aa "
card = card.replace(' ', '')
print(card)