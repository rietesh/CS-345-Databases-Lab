# # -*- coding: UTF-8 -*-
# from cassandra.cluster import Cluster
# import json, os
# import datetime as mod_datetime
# try:
#     cluster = Cluster()
# except:
#     print("couldn't connect to the localhost cluster")
#     exit()
# try:
#     session = cluster.connect('a1')
# except:
#     print("couldn't connect to the keyspace")
#     exit()
#
# def form_media_list(media_list):
#     out_media_list = {}
#     for i in range(len(media_list)):
#         media_list1 = {}
#         media_list1['media_type'] = str((media_list[str(i)]['media_type']))
#         media_list1['media_url'] = str((media_list[str(i)]['media_url']))
#         media_list1['media_id'] = str((media_list[str(i)]['media_id']))
#         media_list1['display_url'] = str((media_list[str(i)]['display_url']))
#         out_media_list[str(i)] = media_list1
#     return out_media_list
#
#
# session.execute("drop table if exists t_for_top")
#
#
# query7 = "create table t_for_top ( " \
#         "location varchar," \
#         "quote_count int," \
#         "reply_count int," \
#         "hashtag varchar," \
#         "datetime timestamp," \
#         "date_tweet date," \
#         "like_count int," \
#         "verified boolean," \
#         "sentiment int," \
#         "author varchar," \
#         "tid varchar," \
#         "retweet_count int," \
#         "tweet_type varchar," \
#         "media_list map<text,frozen<map<text,text>>>," \
#         "quoted_source_id varchar," \
#         "url_list list<varchar>," \
#         "tweet_text varchar," \
#         "author_profile_image varchar," \
#         "author_screen_name varchar," \
#         "author_id varchar," \
#         "lang varchar," \
#         "keywords_processed_list list<varchar>," \
#         "retweet_source_id varchar," \
#         "mentions list<varchar>," \
#         "replyto_source_id varchar," \
#         "hashcnt int," \
#         "PRIMARY KEY ((date_tweet),hashcnt,tid)) WITH CLUSTERING ORDER BY(hashcnt DESC);"
#
# session.execute(query7)
#
# directory = 'ds/'
# count =0
# count2 =0
# for file_name in (os.listdir(directory)):
#     file_data = open(os.path.join(directory, file_name)).read()
#     read_data = json.loads(file_data)
#     for key in read_data.keys():
#         read = read_data[key]
#         location = read['location']
#         quote_count = read['quote_count']
#         reply_count = read['reply_count']
#         hashtags = read['hashtags']
#         datetime = read['datetime']
#         date_tweet = read['date']
#         like_count = read['like_count']
#         verified = True if read['verified'] else False
#         sentiment = read['sentiment']
#         author = read['author']
#         tid = read['tid']
#         retweet_count = read['retweet_count']
#         tweet_type = read['type']
#         media_list = form_media_list(read['media_list']) if read['media_list'] is not None else None
#         quoted_source_id = read['quoted_source_id']
#         url_list = read['url_list']
#         tweet_text = read['tweet_text']
#         author_profile_image = read['author_profile_image']
#         author_screen_name = read['author_screen_name']
#         author_id = read['author_id']
#         lang = read['lang']
#         keywords_processed_list = read['keywords_processed_list']
#         retweet_source_id = read['retweet_source_id']
#         mentions = read['mentions']
#         replyto_source_id = read['replyto_source_id']
#         date_insert = date_tweet
#         if hashtags is not  None:
#             for i in range(0,7):
#                 for j in hashtags:
#                     if not j=='':
#                         print(j)
#                         curcount = session.execute("select count(*) from t_for_top where date_tweet='" + date_insert + "'and hashtag='"  + j + "' allow filtering" )
#                         print(curcount)
#                         for i in curcount:
#                             print(i.count)
#                         # session.execute(
#                         #     """ INSERT INTO t_for_top (location,quote_count,reply_count,hashtags,datetime,date_tweet,like_count,verified,sentiment,author,tid,retweet_count,tweet_type,media_list,quoted_source_id,url_list,tweet_text,author_profile_image,author_screen_name,author_id,lang,keywords_processed_list,retweet_source_id,mentions,replyto_source_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,
#                         #                              (location,quote_count,reply_count,hashtags,datetime,date_insert,like_count,verified,sentiment,author,tid,retweet_count,tweet_type,media_list,quoted_source_id,url_list,tweet_text,author_profile_image,author_screen_name,author_id,lang,keywords_processed_list,retweet_source_id,mentions,replyto_source_id)
#                         # )
#                         break
#                     tmp_Date = mod_datetime.datetime.strptime(date_insert,"%Y-%m-%d").date() + mod_datetime.timedelta(days=1)
#                 print(date_insert)
#                 break
#                 date_insert = tmp_Date.strftime('%Y-%m-%d')
#                 count2 = count2+1
#             # print(count2)
#             count = count+1
#             break
#     break
#     print(count,count2)
#
# -*- coding: UTF-8 -*-
from cassandra.cluster import Cluster
import json, os
import datetime as mod_datetime

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


session.execute("drop table if exists t_for_top")


query5 = "create table t_for_top ( " \
        "hashtag varchar," \
        "date_tweet date," \
        "hashcnt counter," \
        "PRIMARY KEY ((date_tweet),hashtag)) WITH CLUSTERING ORDER BY(hashtag DESC);"

session.execute(query5)

directory = 'ds/'
count =0
count2 =0
for file_name in (os.listdir(directory)):
    file_data = open(os.path.join(directory, file_name)).read()
    read_data = json.loads(file_data)
    for key in read_data.keys():
        read = read_data[key]
        hashtags = read['hashtags']
        date_tweet = read['date']
        date_insert = date_tweet
        if hashtags is not None:
            for hashtag in hashtags:
                if not hashtag == '':
                    for i in range(0, 7):
                        curcount = session.execute("select count(*) from t_for_top where date_tweet='" + date_insert + "'and hashtag='"  + hashtag + "'" )
                        for i in curcount:
                            curcount = i.count
                            break
                        session.execute("UPDATE t_for_top SET hashcnt = hashcnt + 1 WHERE date_tweet='" + date_insert+ "'and hashtag='"  + hashtag + "'")
                        tmp_Date = mod_datetime.datetime.strptime(date_insert,"%Y-%m-%d").date() + mod_datetime.timedelta(days=1)
                        date_insert = tmp_Date.strftime('%Y-%m-%d')
                        count2 = count2 +1
        count = count+1
    print(count,count2)