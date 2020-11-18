#coding=utf8
import sys
import requests
from lxml import etree
from collections import defaultdict
import re
from urllib.parse import urljoin
import sys
import time
from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    # 设置为开发者模式，防止网站识别
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument("--headless")
    # 加载驱动程序
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                                Object.defineProperty(navigator, 'webdriver', {
                                get: () => undefined
                                })
                            """
    })
    return driver

#获取html文本
def get_html(url,switch):
    if switch:
        driver.get(url)

        time.sleep(3)
        ps = driver.page_source
        # driver.quit()
        return ps
    else:
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
        if 'href' not in href.attrib:
            continue
        # if href.text in [u'下一页', 'next']:
        #     next_page_url = href.attrib['href']
        parent = href.xpath('..')
        path = []
        # 递归调用父节点，得到路径
        i=0
        while (len(parent) > 0):
            if i==0:
                class_name=False
            else:
                class_name = parent[0].attrib.get('class')
            i+=1
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
def k_to_xpath(k,endstr):
    best_k = k.split()
    best_k.reverse()
    best_path = "".join(best_k)
    end_path = best_path + endstr
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
    xpath_str = k_to_xpath(k,"/a/@href")
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
def get_best_path_by_contentnum(d):
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

    end_path = k_to_xpath(best_k,"/a/@href")
    print("best_path")
    print(end_path)
    return end_path

def get_best_path_by_total_num(d):
    best_k = 0
    best_v = 0

    for k, v in d.items():
        k_xpath = k_to_xpath(k,"/a//text()")
        k_num = len(base_tree.xpath(k_xpath))
        if k_num==0:
            continue
        k_txt_str = "".join(base_tree.xpath(k_xpath))
        k_txt_list = re.compile("\w+").findall(k_txt_str)
        k_txt_str = "".join(k_txt_list)
        ktxt_num = len(k_txt_str)
        txt_a_ratio = ktxt_num/k_num
        print(k_xpath)
        print(k_txt_str)
        print(ktxt_num)
        print(txt_a_ratio)
        print("------------------")

        if txt_a_ratio > best_v:
            print(best_v,"123")
            best_k = k
            best_v = txt_a_ratio


    print(best_v)
    end_path = k_to_xpath(best_k,"/a/@href")
    print("best_xpath  is   ",end_path)
    return end_path

def go():
    d = get_all_path(base_ps)    #获取所有a链接路径
    if not d:   #处理url 404等错误
        print("没有获取到数据")
        writedata = base_url+"没有获取到数据"+"\n"
        return writedata
    best_path = get_best_path_by_total_num(d)    #获取最优路径


    print('*********')
    linelist = base_tree.xpath(best_path)
    print(linelist)
    print(len(linelist))
    writedata = base_url+"------"+best_path+"------"+str(linelist)+"\n"
    return writedata

def go1():
    global driver
    global base_url
    global base_tree
    global base_ps
    end_file = open("测试结果4.txt", "wb")
    ceshifile = open("456.txt", "rb")
    urllist = ceshifile.readlines()
    driver = get_driver()
    for ii in urllist:
        ii_url = ii.decode("utf-8")
        base_url = ii_url.strip()
        print(base_url)
        try:
            base_ps = get_html(base_url, True)  # 获取html文本
            base_tree = etree.HTML(base_ps)
            writedata = go()
        except:
            writedata = base_url + "没有获取到数据" + "\n"
        end_file.write(writedata.encode("utf-8"))
        end_file.flush()
    end_file.close()

def go2():
    global driver
    global base_url
    global base_tree
    global base_ps
    driver = get_driver()
    base_url = "http://www.moe.gov.cn/jyb_xxgk/moe_1777/moe_1779/"
    base_ps = get_html(base_url, True)  # 获取html文本
    base_tree = etree.HTML(base_ps)
    writedata = go()

if __name__=="__main__":
    go1()
