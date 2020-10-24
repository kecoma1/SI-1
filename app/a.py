import json
import os
import sys

with open('catalogue/catalogue.json', 'r') as myfile:
    data=myfile.read()

# parse file
catalogue = json.loads(data)

print(catalogue['peliculas'][0])

print(catalogue['peliculas'][0]['id'])
for films in catalogue['peliculas']:
    print('aaaaaaaaaaaa    '+str(films['id']))

dir_path = homedir = os.path.expanduser("~")
dir_path += "/public_html/usuarios"
print(dir_path)

card = "a a a aa a aa "
card = card.replace(' ', '')
print(card)

carrito_films = []

i = 0
while i<3:
    carrito_films.append(i)
    print(carrito_films[i])
    i += 1