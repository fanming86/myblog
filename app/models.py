#coding:utf-8

from app import db

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import json,uuid



class Article(db.Model):
    __tablename__ = "article"
    article_id = db.Column(db.Integer, primary_key=True,)
    article_name = db.Column(db.String(64), unique=True)
    article_time = db.Column(db.DateTime)
    article_click = db.Column(db.Integer, unique=True)
    sort_article_id = db.Column(db.Integer,unique=True)
    user_id = db.Column(db.Integer, unique=True)
    article_type = db.Column(db.Integer, unique=True)
    article_content = db.Column(db.Text, unique=True)
    article_up = db.Column(db.Integer, unique=True)
    article_support = db.Column(db.Integer, unique=True)


    def __init__(self,article_id,article_name,article_time,article_click,sort_article_id,user_id,article_type,article_content,article_up,article_support):
        self.article_id =article_id
        self.article_name =article_name
        self.article_time =article_time
        self.article_click =article_click
        self.sort_article_id =sort_article_id
        self.user_id =user_id
        self.article_type =article_type
        self.article_content =article_content
        self.article_up =article_up
        self.article_support = article_support