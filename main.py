import requests
from bs4 import BeautifulSoup
import urllib.request
import json
req = requests.get('https://rainbow6.ubisoft.com/siege/ko-kr/game-info/operators.aspx')
html = req.text
soup = BeautifulSoup(html, 'html.parser')

divs = soup.select("div[data-key]")

result = []
picture = []
logo = []
for div in divs:
    result.append(div['data-key'])
    images = div.findAll('img')
    picture.append(images[0]['src'])
    logo.append(images[1]['src'])
    urllib.request.urlretrieve(images[0]['src'], './'+div['data-key']+'_picture'+'.png')
    urllib.request.urlretrieve(images[1]['src'], './'+div['data-key']+'_logo'+'.png')
print(result)
print(picture)
print(logo)
with open("op.json", "w") as w:
    json.dump(result, w)