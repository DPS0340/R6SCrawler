import urllib

import requests
from bs4 import BeautifulSoup
import json
req = requests.get('https://rainbowsix.fandom.com/wiki/Category:Weapons_of_Tom_Clancy%27s_Rainbow_Six_Siege')
html = req.text
soup = BeautifulSoup(html, 'html.parser')

divs = soup.find_all("li", class_="category-page__member")

result = []
for div in divs:
    context = div.find('a')['title']
    if "Template" not in context:
        result.append("gun_" + context.replace("/Siege", "").replace(" ", "_").replace("-", "_").replace(".", "").lower())
        req2 = requests.get('https://rainbowsix.fandom.com/wiki/%s' % context.replace(" ", "_"))
        html2 = req2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        uri = soup2.find("figure", class_="pi-item pi-image").find('img')['src']
        urllib.request.urlretrieve(uri, './gun/' + "gun_" + context.replace("/Siege", "").replace(" ", "_").replace("-", "_").replace(".", "").lower() + '.jpg')
print(result)
with open("gun.json", "w") as w:
    json.dump(result, w)