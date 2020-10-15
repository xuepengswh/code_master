#coding:utf-8
from selenium import webdriver
import time

options = webdriver.ChromeOptions()

#设置为开发者模式，防止网站识别
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--headless")

# 加载驱动程序


browser = webdriver.Chrome(options=options)

browser.set_script_timeout(0.1)

browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
# browser = webdriver.Chrome()

url = "https://www.nmpa.gov.cn/xxgk/ggtg/index.html"
url2 = "https://www.nmpa.gov.cn/xxgk/ggtg/hzhpchj/hzhpgjjgg/20201013172912157.html"
browser.get(url2)
time.sleep(3)
ps = browser.page_source
browser.quit()
print(ps)
