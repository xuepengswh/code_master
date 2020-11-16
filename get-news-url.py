#coding=utf8
import sys
import requests
from lxml import etree
from collections import defaultdict

url = sys.argv[1]
html = requests.get(url)
html.encoding = html.apparent_encoding
#print(html.text)
page = etree.HTML(html.text)
hrefs = page.xpath("//a")

d = defaultdict(list)
next_page_url = ''
for href in hrefs:
    if href.text == None or href.text.strip() == '':
        continue
    if 'href' not in href.attrib:
        continue
    if href.text in [u'下一页','next']:
        next_page_url = href.attrib['href']
    parent = href.xpath('..')
    path = []
    # 递归调用父节点，得到路径
    while(len(parent) > 0 ):
        div_class = parent[0].attrib.get('class','')
        path.append(parent[0].tag+div_class)
        parent = parent[0].xpath('..')
    path = ' '.join(path)
    text = href.text.strip()
    url = href.attrib['href']
    d[path].append((text,url))

# 便利所有路径，选择文本内容最多的路径作为新闻列表的路径
best_k = ''
best_v = ''
for k,v in d.items():
    text = ' '.join(e[0] for e in v)
    if len(text) > len(best_v):
        best_k = k
        best_v = text
for e in d[best_k]:
    print(e[0],e[1])
print('*********')
print(next_page_url)
