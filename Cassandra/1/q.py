"select date_tweet, count(hashtag) as cnt from t_by_hashtag1 where date_tweet in ('2018-1-16', '2018-1-15', '2018-1-17') and hashtag = 'AusOpen' group by date_tweet;"
