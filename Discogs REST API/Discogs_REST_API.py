import requests
import sys
import time

#Budka Suflera ID: 359282
#Queens Of The Stone Age ID: 56168

try:
    id = int(input('Eneter band ID: '))
except:
    print('Bad ID')

page_url = 'https://api.discogs.com/artists/' + str(id)

page = requests.get(page_url)

if int(page.headers.get('X-Discogs-Ratelimit-Remaining')) == 0:
    print('Rate limit achived, please wait 1 min..')
    time.sleep(60)

if page.status_code != 200 | page.status_code != 429:
    print("Bad server status")
    sys.exit(1)

membersList = page.json()['members']

names = {}

for i in membersList:
    bands = []
    getBand = requests.get(i['resource_url'])
    if int(getBand.headers.get('X-Discogs-Ratelimit-Remaining')) == 0:
        print('Rate limit achived, please wait 1 min..')
        time.sleep(60)
    try:
        for j in getBand.json()['groups']:
            bands.append(j['name'])
        names[i['name']] = bands
    except: pass


result = {}
bands = []

for i in names:
    for j in names[i]:
        bands.append(j)

bands = set(bands)
bands = list(bands)

for i in bands:
    result[i] = []

for i in names:
    for j in names[i]:
        if j in bands:
            result[j].append(i)

for i in sorted(result):
    if len(result[i]) >= 2:
        print('Band:', i, '|| Members:', result[i])

sys.exit(0)
