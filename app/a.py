import json
import os
import sys

with open('catalogue/catalogue.json', 'r') as myfile:
    data=myfile.read()

# parse file
catalogue = json.loads(data)

print(catalogue['peliculas'][0])
