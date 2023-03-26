import requests
import sys
import time

# Budka Suflera ID: 359282
# Queens Of The Stone Age ID: 56168

try:
    id = int(input('Eneter band ID: ')) # entering oryginal band id
except Exception:
    print('Bad ID')

page_url = 'https://api.discogs.com/artists/' + str(id) # creating url

page = requests.get(page_url) # making a request

if int(page.headers.get('X-Discogs-Ratelimit-Remaining')) == 0:
    print('Rate limit achived, please wait 1 min..')
    time.sleep(60)

if page.status_code != 200 | page.status_code != 429:
    print("Bad server status")
    sys.exit(1)

membersList = page.json()['members'] # getting list of oryginal band's members

names = {} # dictionary with members and all their bands

# filling the names dictionary:
for member in membersList:
    bandNames = []
    getBand = requests.get(member['resource_url'])
    if int(getBand.headers.get('X-Discogs-Ratelimit-Remaining')) == 0:
        print('Rate limit achived, please wait 1 min..')
        time.sleep(60)
    try:
        for band in getBand.json()['groups']:
            bandNames.append(band['name'])
        names[member['name']] = bandNames
    except Exception: 
        pass

# putting all band names into list:
bands = []
for member, band in names.items(): 
    bands += band

bands = list(set(bands)) # removing duplicates

# making empty list as a value of result dicttionary:
result = {i: [] for i in bands}

# filling the result dictionary with band name as a key and list of members from oryginal band as value:
for member in names:
    for band in names[member]:
        if band in bands:
            result[band].append(member)

# sorting alphabetically band names and dropping those bands that have only one member from oryginal band
for band in sorted(result):
    if len(result[band]) >= 2:
        print('Band:', band, '|| Members:', result[band])

sys.exit(0)
