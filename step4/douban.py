# -*- coding: utf-8 -*-
import os
from datetime import datetime

import requests
from BeautifulSoup import BeautifulSoup

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def douban(city='beijing'):
    """
    访问豆瓣并返回北京正在上映的电影的的电影名称列表并存入 SQLite
    """

    #数据库设置
    engine = create_engine('sqlite:///movie.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()

    # Movie 的数据库模型
    class Movie(Base):
        __tablename__ = 'movie'

        mid = Column(Integer, primary_key=True)
        name = Column(String(255))
        create_time = Column(DateTime, default=datetime.now)


        def __init__(self, *args, **kwargs):
            super(Movie, self).__init__(*args, **kwargs)

        def __repr__(self):
            return '<Movie %s>' % self.id

    #输出当前文件路径到 path
    path = os.path.abspath(os.path.dirname(__file__))

    #检查文件夹下是否有 movie.sqlite, 如果没有就创建并初始化数据库
    if not os.path.isfile(os.path.join(path,'movie.sqlite')):
        Base.metadata.create_all(engine)

    #GET请求
    r = requests.get('http://movie.douban.com/nowplaying/%s/' % city)
    print '访问结果: %i' %r.status_code

    #把网页内容实例化BeautifulSoup当中
    movie_list = BeautifulSoup(''.join(r.text))

    #取出来所有的 ll 的 span 标签 (内涵上映的电影名称)
    for movie in movie_list.findAll("span", { "class" : "ll" }):

        #取出来 a 锚点的 title 并去掉空格和换行
        name = ''.join(movie.findAll(text=True)).replace(' ', '').replace('\n', '')

        #实例化 Movie
        movie = Movie(name=name)
        #把 movie 存进 db

        #判断是否重复电影名
        exists = session.query(Movie).filter(Movie.name == name).first()
        if not exists:
            #如果不重复保存数据库
            session.add(movie)
            session.commit()
            print '%s 已保存' % name.encode('utf-8')
        else:
            #如果重复就跳过
            print '%s 曾经已保存' % name.encode('utf-8')
            pass


if __name__ == '__main__':
    douban('beijing')