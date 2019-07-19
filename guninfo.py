import requests
from bs4 import BeautifulSoup
import json
import re

urls = ['/rainbowsix/L85A2', '/rainbowsix/AR33', '/rainbowsix/G36C', '/rainbowsix/R4-C', '/rainbowsix/556xi', '/rainbowsix/F2', '/rainbowsix/AK-12', '/rainbowsix/AUG_A2', '/rainbowsix/552_Commando', '/rainbowsix/416-C_Carbine', '/rainbowsix/C8-SFW', '/rainbowsix/Mk17_CQB', '/rainbowsix/PARA-308', '/rainbowsix/Type-89', '/rainbowsix/C7E', '/rainbowsix/M762', '/rainbowsix/V308', '/rainbowsix/Spear_.308', '/rainbowsix/AR-15.50', '/rainbowsix/M4', '/rainbowsix/AK-74M', '/rainbowsix/ARX200', '/rainbowsix/F90', '/rainbowsix/Commando_9', '/rainbowsix/FMG-9', '/rainbowsix/MP5K', '/rainbowsix/UMP45', '/rainbowsix/MP5', '/rainbowsix/P90', '/rainbowsix/9x19VSN', '/rainbowsix/MP7', '/rainbowsix/9mm_C1', '/rainbowsix/MPX', '/rainbowsix/M12', '/rainbowsix/MP5SD', '/rainbowsix/PDW9', '/rainbowsix/Vector_.45_ACP', '/rainbowsix/T-5_SMG', '/rainbowsix/Scorpion_EVO_3_A1', '/rainbowsix/K1A', '/rainbowsix/Mx4_Storm', '/rainbowsix/AUG_A3', '/rainbowsix/P10_RONI', '/rainbowsix/M590A1', '/rainbowsix/M1014', '/rainbowsix/SG-CQB', '/rainbowsix/SASG-12', '/rainbowsix/M870', '/rainbowsix/Super_90', '/rainbowsix/SPAS-12', '/rainbowsix/SPAS-15', '/rainbowsix/SuperNova', '/rainbowsix/ITA12L', '/rainbowsix/SIX12', '/rainbowsix/SIX12_SD', '/rainbowsix/FO-12', '/rainbowsix/BOSG.12.2', '/rainbowsix/ACS12', '/rainbowsix/TCSG12', '/rainbowsix/417', '/rainbowsix/OTs-03', '/rainbowsix/CAMRS', '/rainbowsix/SR-25', '/rainbowsix/Mk_14_EBR', '/rainbowsix/6P41', '/rainbowsix/G8A1', '/rainbowsix/M249', '/rainbowsix/T-95_LSW', '/rainbowsix/LMG-E', '/rainbowsix/ALDA_5.56', '/rainbowsix/M249_SAW', '/rainbowsix/P226_Mk_25', '/rainbowsix/M45_MEUSOC', '/rainbowsix/5.7_USG', '/rainbowsix/P9', '/rainbowsix/LFP586', '/rainbowsix/GSh-18', '/rainbowsix/PMM', '/rainbowsix/P12', '/rainbowsix/Mk1_9mm', '/rainbowsix/D-50', '/rainbowsix/PRB92', '/rainbowsix/P229', '/rainbowsix/USP40', '/rainbowsix/Q-929', '/rainbowsix/RG15', '/rainbowsix/Bailiff_410', '/rainbowsix/Keratos_.357', '/rainbowsix/1911_TACOPS', '/rainbowsix/P-10C', '/rainbowsix/.44_Mag_Semi-Auto', '/rainbowsix/SDP_9mm', '/rainbowsix/SMG-11', '/rainbowsix/Bearing_9', '/rainbowsix/C75_Auto', '/rainbowsix/SMG-12', '/rainbowsix/SPSMG9', '/rainbowsix/ITA12S', '/rainbowsix/Super_Shorty']

result = {}

for url in urls: # url 반복

    uri = 'https://liquipedia.net%s' % url
    print(uri) # Prints the values to a stream

    req = requests.get(uri) # hr = requests.get('https://www.python.org')
    html = req.text #  print? (r.text)
    soup = BeautifulSoup(html, 'html.parser')
    name = uri.split("/")[-1]

    dic = {}
    print(url)
    first_table = soup.find("div", class_="fo-nttax-infobox wiki-bordercolor-light")
    keys = list(map(lambda x: x.text.strip(), first_table.find_all("div", "infobox-cell-2 infobox-description")))

    values = list(map(lambda x: x.text.split("(")[0].strip().replace("\xa0PVP", ""), list(filter(lambda y: "infobox-description" not in y['class'], first_table.find_all("div", class_='infobox-cell-2')))))

    for i in range(len(keys)-1):
        dic[keys[i]] = values[i]
    
    found = list(filter(lambda y: "infobox-description" not in y['class'], first_table.find_all("div", class_='infobox-cell-2')))[-1]
    users = list(map(lambda x: x['title'], found.find_all("a")))

    dic['user(s)'] = users
    
    second_table = soup.find("table", class_="wikitable")

    Attatchments = {}

    tds = second_table.find_all("td")
    keys = []
    for i in range(len(tds)):
        if i % 2 == 0:
            keys.append(tds[i].text.replace("\n", ""))
    values = []
    a = second_table.find_all("a")
    for i in range(len(a)):
        values.append(a[i].text.replace("\n", ""))

    for i in range(len(keys)):
        Attatchments[keys[i]] = values[i]
    
    dic["Attatchments"] = Attatchments
    print(dic)
    
    result[name] = dic

with open("guninfo.json", "w") as w:
    json.dump(result, w)