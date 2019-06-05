#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 0003 18:10
# @Author  : Zzy
# @Site    : 
# @File    : Douban_top250.py
# @Software: PyCharm

# 爬取豆瓣top250排行信息
import requests
from lxml import etree
from bs4 import BeautifulSoup
import os
import csv


# 获取HTML页面
def getHtmlurl(url, header):
    try:
        r = requests.get(url, header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('获取HTML页面失败')
        return ""


# 获取网站图片url,并下载
def get_pictul(html):
    # 使用Beautifulsoup库解析Requests库请求的网页，并提取过滤数据
    soup = BeautifulSoup(html, 'html.parser')
    img_url_list = soup.find_all('img')
    for img in img_url_list:
        url_pic = img.get('src')
        root = 'D:/douban_pic/'
        path = root + url_pic.split('/')[-1]
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(url_pic)
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
        except:
            print('-' * 60)
            # print(url_pic)

# 获取网站信息，并保存到csv文件中
def get_data(html, writer):
    # 使用Lxml的etree库，利用etree.HTML进行初始化，将HTML文档解析为Element对象
    selector = etree.HTML(html)
    # 匹配节点，返回列表
    infos = selector.xpath('//tr[@class="item"]')
    for info in infos:
        # 从当前匹配选择的当前节点选择文档中的节点，不考虑位置
        name = info.xpath('td/div/a/@title')[0]
        url = info.xpath('td/div/a/@href')
        book_infos = info.xpath('td/p/text()')[0]
        author = repr(book_infos).split('/')[0]
        publisher = repr(book_infos).split('/')[-3]
        date = repr(book_infos).split('/')[-2]
        price = repr(book_infos).split('/')[-1]
        rate = info.xpath('td/div/span[2]/text()')[0]
        comments = info.xpath('td/div/span/text()')
        comment = comments[0] if len(comments) != 0 else '空'
        writer.writerow((name, url, author, publisher, date, price, rate, comment))


# 构造csv Writer对象，并写入
def Writer_data():
    root = 'D:/Douban250_data/'
    path = root + 'zzy.csv'
    if not os.path.exists(root):
        os.mkdir(root)
    fp = open(path, 'a', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    writer.writerow(('name', 'url', 'author', 'publisher', 'date', 'price', 'rate', 'comment'))
    return writer


# 主函数
def main(url, header):
    # 分页，构造URL列表。
    url_list = [url + '?start={}'.format(str(i)) for i in range(0, 250, 25)]
    for i in range(len(url_list)):
        print("wait~~~~~~~~~~~~~~~~~~~~~~~~~")
        html = getHtmlurl(url_list[i], header)
        get_data(html, Writer_data())
        get_pictul(html)
        print(['第{}面'.format(i + 1) + '保存成功'][0])


if __name__ == '__main__':
    url = 'https://book.douban.com/top250'
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'}
    main(url, header)
