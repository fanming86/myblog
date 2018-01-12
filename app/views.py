# coding:utf-8

from flask import render_template, url_for, request, flash, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
import time
import sys, json
from app import app, db, lm
from models import Article
from .forms import LoginForm, Register

reload(sys)
sys.setdefaultencoding('utf8')


@app.route("/")
def index():
    article = Article.query.all()
    return render_template("index.html", article=article)


@app.route('/about', methods=['POST', 'GET'])
def about():
    article = Article.query.all()
    return render_template("about.html", article=article)


@app.route('/article/<int:ar_id>')
def article(ar_id):
    articles = Article.query.filter(Article.article_id == ar_id).first()
    # return articles.article_content
    return render_template('article.html',articles=articles)


@app.errorhandler(404)
def page_not_found(e):
    myname = None
    if 'user_id' in session:
        myname = session['username']
    return render_template('404.html', myname=myname), 404


@app.errorhandler(500)
def internal_server_error(e):
    myname = None
    if 'user_id' in session:
        myname = session['username']
    return render_template('500.html', myname=myname), 500
