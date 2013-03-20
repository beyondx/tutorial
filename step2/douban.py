# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup


def douban():
    """
    访问豆瓣并返回北京正在上映的电影的的 title 内容
    """

    #GET请求
    r = requests.get('http://movie.douban.com/nowplaying/beijing/')
    #获得 HTTP 状态码
    print r.status_code
    #把网页内容实例化BeautifulSoup当中
    nowplaying = BeautifulSoup(''.join(r.text))
    #提取 网页标题
    print nowplaying.html.head.title.string.encode('utf-8')

if __name__ == '__main__':
    douban()