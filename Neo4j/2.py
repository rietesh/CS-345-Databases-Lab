import os,json
import csv

directory = 'ds/'
for file_name in (os.listdir(directory)):
    file_data = open(os.path.join(directory, file_name)).read()
    read_data = json.loads(file_data)
    for key in read_data.keys():
        read = read_data[key]
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
        media_list = read['media_list'] if read['media_list'] is not None else None
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

        with open('a.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([tid,author_id ])