# -*- coding:utf-8 -*-
from flask import Flask, render_template,request
from lxml import etree
import json
from get_xpath import get_xpath_through_average
from get_xpath import get_xapth_through_total
from get_xpath import get_all_path
from get_xpath import download_data

app = Flask(__name__)

def get_xpath_data(url,ttype,selenium):
    ps = download_data.get_html(url,selenium)
    base_tree = etree.HTML(ps)
    d = get_all_path.get_all_path(base_tree)
    if ttype==1:
        xpath_str = get_xpath_through_average.get_best_path(d)
    else:
        xpath_str = get_xapth_through_total.get_best_path(d)
    return xpath_str

@app.route('/aver',methods=['post'])
def aver():
    url = request.values.get('url')
    selenium =  request.values.get('selenium')
    result = get_xpath_data(url,1,selenium)

    xpath_str = result['xpath']
    detail = result['detail']
    text = detail['text']
    href = detail['href']
    return render_template('linelist.html', xpath_str=xpath_str, text=text, href=href)

@app.route('/total',methods=['post'])
def tatal():
    url = request.values.get('url')
    selenium = request.values.get('selenium')
    result = get_xpath_data(url, 2,selenium)

    xpath_str = result['xpath']
    detail = result['detail']
    text = detail['text']
    href = detail['href']
    return render_template('linelist.html', xpath_str=xpath_str, text=text, href=href)

@app.route('/',methods=['get'])
def index():
    return render_template('linelist.html')


if __name__ == '__main__':
    app.run(port=5001, debug=True)

