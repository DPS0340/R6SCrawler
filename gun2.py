import urllib

import requests
from bs4 import BeautifulSoup
import json
req = requests.get('https://liquipedia.net/rainbowsix/Portal:Weapons')
html = req.text
soup = BeautifulSoup(html, 'html.parser')

divs = soup.find_all("li", class_="gallerybox")

result = []
for div in divs:
    href = div.find('a')['href']
    context = href
    result.append(context.split("/")[-1])
    # uri = div.find("img")['src']
    # urllib.request.urlretrieve("https://liquipedia.net"+uri, './gun2/' + "gun_" + context.replace(" ", "_").replace("-", "_").replace(".", "").lower() + '.png')
print(result)
with open("gun.json", "w") as w:
    json.dump(result, w)