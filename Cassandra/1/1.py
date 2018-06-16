# -*- coding: UTF-8 -*-
from cassandra.cluster import Cluster
import json, os

try:
    cluster = Cluster()
except:
    print("couldn't connect to the localhost cluster")
    exit()
try:
    session = cluster.connect('a1')
except:
    print("couldn't connect to the keyspace")
    exit()

# 1
session.execute("drop table if exists t_by_auth")
# 2
session.execute("drop table if exists t_by_keyword")
# 3
session.execute("drop table if exists t_by_hashtag")
# 4
session.execute("drop table if exists t_by_mention")
# 5
# session.execute("drop table if exists t_by_loc")
# 6
session.execute("drop table if exists t_by_loc")
# 7
# session.execute("drop table if exists t_by_loc")
# 8
session.execute("drop table if exists t_for_delete ")

query1 = "create table t_by_loc ( " \
        "location varchar," \
        "quote_count int," \
        "reply_count int," \
        "hashtags list<varchar>," \
        "datetime timestamp," \
        "date_tweet date," \
        "like_count int," \
        "verified boolean," \
        "sentiment int," \
        "author varchar," \
        "tid varchar," \
        "retweet_count int," \
        "tweet_type varchar," \
        "media_list map<text,frozen<map<text,text>>>," \
        "quoted_source_id varchar," \
        "url_list list<varchar>," \
        "tweet_text varchar," \
        "author_profile_image varchar," \
        "author_screen_name varchar," \
        "author_id varchar," \
        "lang varchar," \
        "keywords_processed_list list<varchar>," \
        "retweet_source_id varchar," \
        "mentions list<varchar>," \
        "replyto_source_id varchar," \
        "PRIMARY KEY ((location),datetime)) WITH CLUSTERING ORDER BY(datetime DESC);"
query6 = "create table t_by_loc ( " \
        "location varchar," \
        "quote_count int," \
        "reply_count int," \
        "hashtags list<varchar>," \
        "datetime timestamp," \
        "date_tweet date," \
        "like_count int," \
        "verified boolean," \
        "sentiment int," \
        "author varchar," \
        "tid varchar," \
        "retweet_count int," \
        "tweet_type varchar," \
        "media_list map<text,frozen<map<text,text>>>," \
        "quoted_source_id varchar," \
        "url_list list<varchar>," \
        "tweet_text varchar," \
        "author_profile_image varchar," \
        "author_screen_name varchar," \
        "author_id varchar," \
        "lang varchar," \
        "keywords_processed_list list<varchar>," \
        "retweet_source_id varchar," \
        "mentions list<varchar>," \
        "replyto_source_id varchar," \
        "PRIMARY KEY ((location),datetime)) WITH CLUSTERING ORDER BY(datetime DESC);"

query6 = "create table t_by_loc ( " \
        "location varchar," \
        "quote_count int," \
        "reply_count int," \
        "hashtags list<varchar>," \
        "datetime timestamp," \
        "date_tweet date," \
        "like_count int," \
        "verified boolean," \
        "sentiment int," \
        "author varchar," \
        "tid varchar," \
        "retweet_count int," \
        "tweet_type varchar," \
        "media_list map<text,frozen<map<text,text>>>," \
        "quoted_source_id varchar," \
        "url_list list<varchar>," \
        "tweet_text varchar," \
        "author_profile_image varchar," \
        "author_screen_name varchar," \
        "author_id varchar," \
        "lang varchar," \
        "keywords_processed_list list<varchar>," \
        "retweet_source_id varchar," \
        "mentions list<varchar>," \
        "replyto_source_id varchar," \
        "PRIMARY KEY ((location),datetime)) WITH CLUSTERING ORDER BY(datetime DESC);"
query6 = "create table t_by_loc ( " \
        "location varchar," \
        "quote_count int," \
        "reply_count int," \
        "hashtags list<varchar>," \
        "datetime timestamp," \
        "date_tweet date," \
        "like_count int," \
        "verified boolean," \
        "sentiment int," \
        "author varchar," \
        "tid varchar," \
        "retweet_count int," \
        "tweet_type varchar," \
        "media_list map<text,frozen<map<text,text>>>," \
        "quoted_source_id varchar," \
        "url_list list<varchar>," \
        "tweet_text varchar," \
        "author_profile_image varchar," \
        "author_screen_name varchar," \
        "author_id varchar," \
        "lang varchar," \
        "keywords_processed_list list<varchar>," \
        "retweet_source_id varchar," \
        "mentions list<varchar>," \
        "replyto_source_id varchar," \
        "PRIMARY KEY ((location),datetime)) WITH CLUSTERING ORDER BY(datetime DESC);"

session.execute(query)

'''
        "quote_count": 0, 
        "reply_count": 0, 
        "hashtags": null, 
        "datetime": "2017-11-26 23:58:51", 
        "date": "2017-11-26", 
        "like_count": 0, 
        "verified": "False", 
        "sentiment": 0, 
        "author": "Judy💯The Resistance", 
        "location": "Hollywood, California USA🇺🇸", 
        "tid": "934934507945312256", 
        "retweet_count": 0, 
        "type": "retweet", 
        "media_list": null, 
        "quoted_source_id": null, 
        "url_list": null, 
        "tweet_text": "RT @kylegriffin1: Reminder: The Senate Judiciary Committee gave Jared Kushner a November 27 deadline to turn over the missing records… ", 
        "author_profile_image": "https://pbs.twimg.com/profile_images/922041668496265216/uV8jwota_normal.jpg", 
        "author_screen_name": "jgirl66", 
        "author_id": "23737528", 
        "lang": "en", 
        "keywords_processed_list": [
            "reminder", 
            "senate judiciary committee", 
            "kushner november", 
            "deadline"
        ], 
        "retweet_source_id": "934872065471115264", 
        "mentions": [
            "kylegriffin1"
        ], 
        "replyto_source_id": null
    }
'''

def form_media_list(media_list):
    out_media_list = {}
    for i in range(len(media_list)):
        media_list1 = {}
        media_list1['media_type'] = str((media_list[str(i)]['media_type']))
        media_list1['media_url'] = str((media_list[str(i)]['media_url']))
        media_list1['media_id'] = str((media_list[str(i)]['media_id']))
        media_list1['display_url'] = str((media_list[str(i)]['display_url']))
        out_media_list[str(i)] = media_list1
    return out_media_list

directory = 'ds/'
count =0
for file_name in (os.listdir(directory)):
    file_data = open(os.path.join(directory, file_name)).read()
    read_data = json.loads(file_data)
    for key in read_data.keys():
        read = read_data[key]
        # print(read['location'])
        location = 'none' if read['location'] is None else read['location']
        quote_count = read['quote_count']
        reply_count = read['reply_count']
        hashtags = read['hashtags']
        datetime = read['datetime']
        date_tweet = read['date']
        like_count = read['like_count']
        verified = True if read['verified'] else False
        sentiment = read['sentiment']
        author = read['author']
        tid = read['tid']
        retweet_count = read['retweet_count']
        tweet_type = read['type']
        media_list = form_media_list(read['media_list']) if read['media_list'] is not None else None
        # print(quote_count,reply_count,hashtags,datetime,date_tweet,"vaibz lodu",media_list)
        quoted_source_id = read['quoted_source_id']
        url_list = read['url_list']
        tweet_text = read['tweet_text']
        author_profile_image = read['author_profile_image']
        author_screen_name = read['author_screen_name']
        author_id = read['author_id']
        lang = read['lang']
        keywords_processed_list = read['keywords_processed_list']
        retweet_source_id = read['retweet_source_id']
        mentions = read['mentions']
        replyto_source_id = read['replyto_source_id']
        session.execute(
            """ INSERT INTO t_by_loc (location,quote_count,reply_count,hashtags,datetime,date_tweet,like_count,verified,sentiment,author,tid,retweet_count,tweet_type,media_list,quoted_source_id,url_list,tweet_text,author_profile_image,author_screen_name,author_id,lang,keywords_processed_list,retweet_source_id,mentions,replyto_source_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,
                                     (location,quote_count,reply_count,hashtags,datetime,date_tweet,like_count,verified,sentiment,author,tid,retweet_count,tweet_type,media_list,quoted_source_id,url_list,tweet_text,author_profile_image,author_screen_name,author_id,lang,keywords_processed_list,retweet_source_id,mentions,replyto_source_id)
        )
        count = count+1
    print(count)
        # print key
# print(read)

# insert into a(f1,f2) values (10,{media_type: 'photo',display_url: 'pic.twitter.com/4eFHLCNsak', media_id: '933711432725573634',media_url: 'https://pbs.twimg.com/ext_tw_video_thumb/933711432725573634/pu/img/jxzAZ4aDKqgMeFJZ.jpg'});
# insert it like this ie without the '' on lhs

