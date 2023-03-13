import requests
from bs4 import BeautifulSoup
import sys

page_url = 'https://pogoda.onet.pl/prognoza-pogody/krakow-306020'
page = requests.get(page_url)

if page.status_code != 200:
    print("Bad server status")
    sys.exit(1)

if 'text/html' not in page.headers.get('Content-Type'):
    print("Bad type")
    sys.exit(1)

soup = BeautifulSoup(page.content, 'html.parser')

Labels = soup.find_all('span', attrs={'class': 'restParamLabel'})
Values = soup.find_all('span', attrs={'class': 'restParamValue'})

data = {}
dataV = {}
for i in range(7):
    data[Labels[i].text] = Values[i].text

data["Temperatura"] = soup.find('div', attrs={'class': 'temperature'}).text

for i in data:
    val = str(data[i]).split()
    if "%" in val[0]:
        val[0] = val[0].strip('%')
        try:
            val[0] = float(val[0])/100
        except:
            print("Data error")
            sys.exit(1)
    elif "°C" in val[0]:
        val[0] = val[0].strip('°C')
    elif "°" in val[0]:
        val[0] = val[0].strip('°')
    elif "None" in val[0]:
        val[0] = "0"
    elif "," in val[0]:
        val[0] = val[0].replace(",", ".")
    try:
        dataV[i] = float(val[0])
    except:
        print("Data error")
        sys.exit(1)


for i in dataV:
    print(i, ':', dataV[i])

if bytes('Witamy w naszym serwisie pogodowym', "utf-8") not in page.content:
    print("Page error")
    sys.exit(1)

sys.exit(0)
