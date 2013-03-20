# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup


def douban():
    """
    访问豆瓣并返回北京正在上映的电影的的电影名称列表
    """

    #GET请求
    r = requests.get('http://movie.douban.com/nowplaying/beijing/')
    #把网页内容实例化BeautifulSoup当中
    movie_list = BeautifulSoup(''.join(r.text))
    #提取所有电影名称
    #print soup.findAll("span", { "class" : "ll" })
    #从列表中取出来 a 锚点的每个电影名称, 去掉空格和换行(回车)
    for movie in movie_list.findAll("span", { "class" : "ll" }):
        print ''.join(movie.findAll(text=True)).replace(' ', '').replace('\n', '')

if __name__ == '__main__':
    douban()