#coding=utf8
import sys
import requests
from lxml import etree
from collections import defaultdict
import re
from urllib.parse import urljoin
import sys

#获取html文本
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    }
    ps = requests.get(url, headers=headers, verify=False).content.decode("utf-8")
    return ps

#获取所有a链接的路径
def get_all_path(ps):
    page = etree.HTML(ps)
    hrefs = page.xpath("//a")

    d = defaultdict(list)
    for href in hrefs:
        # if href.text == None or href.text.strip() == '':
        #     continue
        if 'href' not in href.attrib:
            continue
        # if href.text in [u'下一页', 'next']:
        #     next_page_url = href.attrib['href']
        parent = href.xpath('..')
        path = []
        # 递归调用父节点，得到路径
        while (len(parent) > 0):
            class_name = parent[0].attrib.get('class')   #改动1
            tag_name = parent[0].tag
            if class_name and class_name.find(" ")==-1:
                path.append("/"+tag_name+"[@class='"+class_name+"']")
            else:
                path.append("/"+tag_name)
            parent = parent[0].xpath('..')
        path = ' '.join(path)
        text = None
        url = href.attrib['href']
        d[path].append((text, url))
    return d

#从k值变成xpath字符串
def k_to_xpath(k):
    best_k = k.split()
    best_k.reverse()
    best_path = "".join(best_k)
    end_path = best_path + "/a/@href"
    return end_path

#获取网页的汉字数量和网页链接数a的比值
def get_num_ratio(ps):
    mytree = etree.HTML(ps)
    txtnum = mytree.xpath("//text()")
    endnum = "".join(txtnum)
    hanzi = re.compile("[\u4e00-\u9fa5]+").findall(endnum)
    hanzi = " ".join(hanzi)
    hanzi = hanzi.replace(" ", "")
    hanzi_num = len(hanzi)
    href_list = mytree.xpath("//a")
    href_num = len(href_list)
    if href_num==0:
        href_num=1
    num_ratio  = hanzi_num/href_num
    print(num_ratio)
    return num_ratio

# 根据k获取网页txt数量
def k_to_txtnum(k):
    xpath_str = k_to_xpath(k)
    mytree = etree.HTML(base_ps)
    url = mytree.xpath(xpath_str)
    if not url: #空列表
        return 0
    url = url[0]
    url = urljoin(base_url,url)
    try:
        ps = get_html(url)
    except:     #网络请求出现错误(gopage)等，返回0
        return 0
    num = get_num_ratio(ps) #网页文字数量和链接数量的比值
    return num

#根据文章字数数量确定链接路径
def get_best_path(d):
    # for k, v in d.items():
    #     print(k, v)
    best_k = 0
    best_v = 0
    for k, v in d.items():
        page_txtnum = k_to_txtnum(k)
        if page_txtnum > best_v:
            best_k = k
            best_v = page_txtnum

    for e in d[best_k]:
        print(e[0], e[1])

    end_path = k_to_xpath(best_k)
    print("best_path")
    print(end_path)
    return end_path

def go():
    d = get_all_path(base_ps)    #获取所有a链接路径
    if not d:   #处理url 404等错误
        print("没有获取到数据")
        return
    best_path = get_best_path(d)    #获取最优路径
    mytree = etree.HTML(base_ps)

    print('*********')
    linelist = mytree.xpath(best_path)
    print(linelist)
    print(len(linelist))

if __name__=="__main__":
    base_url = "http://service.shanghai.gov.cn/XingZhengWenDangKu/XZGFList.aspx?testpara=0&kw=&issueDate_userprop8=&status=0&departid=&wenhao=&issueDate_userprop8_end=&excuteDate=&excuteDate_end=&closeDate=&closeDate_end=&departtypename=&typename=&zhutitypename=&zhuti=&currentPage=1&pagesize=10"
    base_ps = get_html(base_url)  #获取html文本
    go()
