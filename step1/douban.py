# -*- coding: utf-8 -*-
import requests


def douban():
    """
    访问豆瓣并返回北京正在上映的电影的 HTML 文本和 HTTP 状态码
    """

    #GET请求
    r = requests.get('http://movie.douban.com/nowplaying/beijing/')
    #获得 HTTP 状态码
    print r.status_code
    #获得 HTML 文本
    print r.text.encode('utf-8')

if __name__ == '__main__':
    douban()