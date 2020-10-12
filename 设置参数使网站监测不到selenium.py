options = webdriver.ChromeOptions()
    # 设置为开发者模式，防止网站识别
    options.add_experimental_option(
        'excludeSwitches', ['enable-automation'])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")
    # 加载驱动程序
    browser = webdriver.Chrome(executable_path='./chromedriver',
                               options=options)

    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })