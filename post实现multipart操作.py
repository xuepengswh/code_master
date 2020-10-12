import requests
from requests_toolbelt import MultipartEncoder

url = "http://gkml.customs.gov.cn/tabid/1164/default.aspx"

fields = {
    "__EVENTTARGET":(None,"ess$ctr445$ListG_Info$AspNetPager"),
    "__EVENTARGUMENT":(None,"40"),
    "ess$ctr445$ListG_Info$AspNetPager_input":(None,"1"),

}

m=MultipartEncoder(fields = fields)

headers = {
"Content-Type":m.content_type,
}

ps = requests.post(url,data=m,headers=headers).content.decode("utf-8")
print(ps)
