# https://liquipedia.net/rainbowsix/Ash <- 들어가 보시라!

# R6S Dict Operator information Crawler

import requests # 리퀘스트 라이브러리
from bs4 import BeautifulSoup # 파싱 라이브러리 bs4
import json # 데이터 저장용 json
import urllib # 이미지 저장용 urllib

ops = ["nokk", "warden", "mozzie", "gridlock", "nomad", "kaid", "clash", "maverick", "maestro", "alibi", "lion", "finka", "vigil", "dokkaebi", "zofia", "ela", "ying", "lesion", "mira", "jackal", "hibana", "echo", "caveira", "capitao", "blackbeard", "valkyrie", "buck", "frost", "mute", "sledge", "smoke", "thatcher", "ash", "castle", "pulse", "thermite", "montagne", "twitch", "doc", "rook", "jager", "bandit", "blitz", "iq", "fuze", "glaz", "tachanka", "kapkan"]
# 오퍼레이터 데이터

def insider(val):
    # 재귀적으로 html inside text 구하기
    try:
        return insider(val.contents[0].text)
    except:
        return val.text

def parse_gadget(gadget_attrs, gadget_dict):
    gadget_name = insider(gadget_attrs[0]).replace("\n", "") # 유니크 가젯 이름
    gadget_explain = insider(gadget_attrs[1]).replace("\n", "") # 유니크 가젯 설명
    result = {gadget_name: gadget_explain}
    key = unique_gadget_attrs[2].find_all("div")[2].find_all("dd")
    value = unique_gadget_attrs[2].find_all("div")[3].find_all("dd")
    parsed_key = []
    parsed_value = [] # 리스트 초기화
    for attr in key:
        parsed_key.append(insider(attr).replace("\xa0", ""))
    for attr in value:
        parsed_value.append(insider(attr).replace("\xa0", ""))

    for i in range(len(parsed_key)):
        result[parsed_key[i]] = parsed_value[i]
    gadget_dict["unique"] = result

def parse_gadget_name(gadget_attrs, gadget_dict):
    name = insider(gadget_attrs[0]).replace("\n", "")
    gadget_dict["gun_" + name.replace(" ", "_").replace("-", "_").replace(".", "").lower()] = name



result = {} # Result 딕셔너리 생성  

for op in ops: # 오퍼레이터 개별 파싱 반복
    op = op[0].upper() + op[1:] # 오퍼레이터 첫번째 대문자로 변경 -> 리다이렉트 방지
    req = requests.get("https://liquipedia.net/rainbowsix/%s" % op)# op의 문자열을 이용해서 request 날린 다음 req 변수에 저장
    html = req.text # html 변수에 전체 html을 text로 저장
    soup = BeautifulSoup(html, 'html.parser') # bs4를 이용해서 bs4 자체 자료형으로 파싱    
    
    op_info = {} # 개별 오퍼레이터 딕셔너리(파싱이 끝나고 result에 넣을 예정)

    # 우측 표 파싱 단계

    first_table = soup.find("div", class_="fo-nttax-infobox-wrapper") # class는 예약어라서 bs4에서는 class_를 사용
    if first_table is None:
        continue # 아직 정보가 없는 오퍼레이터의 경우에는 continue
    # <div class="fo-nttax-infobox-wrappert">...</div> <- 실제 구조

    key = first_table.find_all("div", class_="infobox-cell-2 infobox-description")
    value = list(filter(lambda div: "infobox-description" not in div['class'], first_table.find_all("div", class_="infobox-cell-2")))
    # filter(lambda div: "infobox-description" not in div['class'], ...) 을 한 이유: infobox-description에는 key가 있기 때문에 중복된 것을 제거하고 value만 남김
    # list(...) -> iterator를 list로 변경

    # key와 value의 경우에는 아직 html 구조의 리스트 -> 본격적인 파싱 단계 시작

    parsed_key = []
    parsed_value = [] # 리스트 생성

    for key_attr in key:
        parsed_key.append(key_attr.text) # ex) Affiliation:
    for value_attr in value:
        parsed_value.append(insider(value_attr).strip()) # ex) SWAT
        # a attribute name을 찾아서 inside text를 반환하는 함수
    
    # 개별 오퍼레이터 딕셔너리 입력
    for i in range(len(parsed_key)): # range 함수로 iterator 생성, i를 index로 설정
        op_info[parsed_key[i]] = parsed_value[i] # {"Affiliation:": "SWAT"}

    # 가젯 & 무기 파싱 단계
    second_tables = soup.find_all("div", class_="template-box") # 가젯 & 무기 테이블 파싱

    if len(second_tables) == 0:
        continue

    unique_gadget_table = second_tables[0] # 가젯 테이블 분리
    unique_gadget_attrs = unique_gadget_table.find_all("tr")
    second_tables = second_tables[1:] # 가젯 테이블 분리

    gadget_dict = {}

    parse_gadget(unique_gadget_attrs, gadget_dict)
    for table in second_tables:
        parse_gadget_name(table.find_all("tr"), gadget_dict)

    op_info['gadget'] = gadget_dict

    result[op.lower()] = op_info
    print(op_info)

with open("opinfo.json", 'w') as w:
    json.dump(result, w)