# -*- coding: UTF-8 -*-
from flask import Flask
from flask import render_template,request
from cassandra.cluster import Cluster
import json, os
import datetime as mod_datetime

app = Flask(__name__)

def session_conn():
    try:
        cluster = Cluster()
    except:
        print("couldn't connect to the localhost cluster")
        raise ("error in localhost connection to cassandra")
    try:
        session = cluster.connect('a1')
    except:
        print("couldn't connect to the keyspace")
        raise ("error in keyspace connection")
    return session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('q1.html')

@app.route('/query/<int:query_id>',methods=['GET', 'POST'])
def show_post(query_id):
    if (query_id == 1):
        if request.method=="GET":
            return render_template('index.html',query=1)
        elif request.method=="POST":
            authorname = request.form.get('authorname')
            status = 0
            output = ''
            error = ''
            if not authorname=='':
                query = "select tid,author,author_screen_name,tweet_text,lang,datetime from t_by_auth where author='" + str(authorname) + "'"
                session = session_conn()
                output = session.execute(query)
                status = 1
            else:
                error="Empty Author Name"
            return render_template('index.html',query=1,request=request,status=status,error=error,output=output)
    if (query_id == 2):
        if request.method=="GET":
            return render_template('index.html',query=2)
        elif request.method=="POST":
            keyword = request.form.get('keyword')
            error = ""
            status = 0
            output = ''
            if not keyword == '':
                query = "select date_tweet,like_count,keyword,tid from t_by_keyword where keyword='" + keyword + "'"
                session = session_conn()
                output = session.execute(query)
                status = 1
            else:
                error = "No Keyword given"
            return render_template('index.html',query=2, request=request, status=status, error=error, output=output)
    if (query_id == 3):
        if request.method=="GET":
            return render_template('index.html',query=3)
        elif request.method=="POST":
            hashtag = request.form.get('hashtag')
            error = ""
            status = 0
            output = ''
            if not hashtag == '':
                query = "select datetime,hashtag,tid from t_by_hashtag where hashtag='" + hashtag + "'"
                session = session_conn()
                output = session.execute(query)
                status = 1
            else:
                error = "No Hashtag given"
            return render_template('index.html',query=3, request=request, status=status, error=error, output=output)
    if (query_id == 4):
        if request.method=="GET":
            return render_template('index.html',query=4)
        elif request.method=="POST":
            author_id = request.form.get('author')
            error = ""
            status = 0
            output = ''
            if not author_id == '':
                query = "select datetime,author_id,tid from t_by_mention where mention='" + author_id + "'"
                session = session_conn()
                output = session.execute(query)
                status = 1
            else:
                error = "No Author given"
            return render_template('index.html',query=4, request=request, status=status, error=error, output=output)
    if (query_id == 5):
        if request.method=="GET":
            return render_template('index.html',query=5)
        elif request.method=="POST":
            date = request.form.get('date')
            error = ""
            status=0
            output = ''
            if not date == '':
                query = "select date_tweet,like_count,tid from t_by_popularity where date_tweet='" + date + "'"
                session = session_conn()
                output = session.execute(query)
                status = 1
            else:
                error = "No Date selected"
            return render_template('index.html',query=5,request=request,status=status,error=error,output=output)
    if (query_id == 6):
        if request.method=="GET":
            return render_template('index.html',query=6)
        elif request.method=="POST":
            location = request.form.get('location')
            status = 0
            error = ''
            output = ''
            if not location=='':
                query = "select tid,location,datetime from t_by_loc where location='" + str(location) + "'"
                session = session_conn()
                status=1
                output = session.execute(query)
            else:
                error = "No Location selected"
            return render_template('index.html',query=6,request=request,status=status,error=error,output=output)
    if (query_id == 7):
        if request.method=="GET":
            return render_template('index.html',query=7)
        elif request.method=="POST":
            date = request.form.get('date')
            status = 0
            error = ''
            output = ''
            if not date == '':
                querydelete = "drop table if exists helper;"
                querycreate = "create table if not exists helper(date_tweet date,hashcnt int,hashtag varchar,primary key(date_tweet,hashcnt,hashtag)) with clustering order by (hashcnt DESC);"
                queryfetch = 'select date_tweet,hashtag,hashcnt from t_for_top'
                session = session_conn()
                status = 1
                output = session.execute(querydelete)
                output = session.execute(querycreate)
                output = session.execute(queryfetch)
                for i in output:
                    date_tweet = str(i.date_tweet)
                    hashtag = (i.hashtag)
                    queryinsert = "insert into helper(date_tweet,hashtag,hashcnt) values ('" + date_tweet + "','" + hashtag + "',"+ str(i.hashcnt) + ");"
                    session.execute(queryinsert)
                # before_date = mod_datetime.datetime.strptime(date, "%Y-%m-%d").date() - mod_datetime.timedelta(days=6)
                # before_date.strftime("%Y-%m-%d")
                queryanswer = "select hashtag from helper where date_tweet='" + str(date) +"' LIMIT 20 "
                output = session.execute(queryanswer)
            else:
                error = "No Location selected"
            return render_template('index.html',query=7, request=request, status=status, error=error, output=output)
    if (query_id == 8):
        if request.method=="GET":
            return render_template('index.html',query=8)
        elif request.method=="POST":
            date = request.form.get('date')
            error=""
            if not date == '':
                query = "delete from t_for_delete where date_tweet='" + date + "'"
                session = session_conn()
                q = session.execute(query)
                # print(q.rowcount)
                # count = q.rowcount
                status = 1
            else:
                error="No Date selected"
                status = 0
            return render_template('index.html',query=8,request=request,error=error,status=status)
