# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup


def douban(city='beijing'):
    """
    访问豆瓣并返回北京正在上映的电影的的电影名称列表并存入 SQLite
    """

    #数据库依赖
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

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

        def __init__(self, *args, **kwargs):
            super(Movie, self).__init__(*args, **kwargs)

        def __repr__(self):
            return '<Movie %s>' % self.id

    #数据库初始化
    #(并不是每次都需要, 待优化)
    Base.metadata.create_all(engine)

    #GET请求
    r = requests.get('http://movie.douban.com/nowplaying/%s/' %city)
    print '访问结果: %i' %r.status_code

    #把网页内容实例化BeautifulSoup当中
    movie_list = BeautifulSoup(''.join(r.text))

    #取出来所有的 ll 的 span 标签 (内涵上映的电影名称)
    for movie in movie_list.findAll("span", { "class" : "ll" }):

        #取出来 a 锚点的title 并去掉空格和换行
        name = ''.join(movie.findAll(text=True)).replace(' ', '').replace('\n', '')

        #实例化 Movie
        movie = Movie(name=name)
        #把 movie 存进 db
        #(重复提交未判断, 待优化)
        session.add(movie)
        session.commit()

        print '%s 已保存' %name.encode('utf-8')


if __name__ == '__main__':
    douban('beijing')