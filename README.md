Coursework research is a research of dependence of suicidal posts in Twitter and official suicide countries rates.

It is mainly directed to examine Tweets' hashtags connected to suicidal thougths, gather data based on Tweets location
or user location if the first one is not pinned. Then, creating statistics by amount of posts in various countries.
The next step is to compare official data and the one that was gathered from Twitter.

FOLDERS 

testing_api

A file testing_api.py is testing Twitter API and abilities, that can be presented by tweepy library
in working with Twitter API. Unfortunately, I cannot share a hidden module in case of private policy, that was signed
when getting Twitter API keys.

It also has functions to write gathered data into .json and .csv files. There are examples of files(testing_api.json and
testing_api.csv) of such formats and you can easily access them.

Warning: testing_api.py is only a TESTING module, that checks work of libraries and modules I use for my research.

Twitter_data.db is database with tweets collected from Twitter with twitter_db.py module help. It has around 
18 thousand tweets with #suicide. twitter_db.py module rewrites data from testing_api.txt file with tweets, forming
a database.

soup

This folder is concentrated mainly on parsing a website with official rates about suicides in various countries.
Official_data.db was formed with beautifulsoup_parsing.py help, where I have used Beautiful Soup library to parse
a table on a website.

geonames

This folder has an ADT in it. ADT_Tweets.py is directed to count amount of tweets in each country. It uses both 
geonames library and created database of cities and its countries to ensure, that the information will be relevant.
Additionally, geonames has limited amount of requests and as a consequence, I had to form Cities_data.db, which 
consists of a country, its cities and code of a country. It was formed with cities_db.py module. Folder has a 
testing_ADT.py module, which actually tests an ADT.

analysis

week_tweets.py module is directed to analyse tweets "behaviour". It is analysing the frequency of posting tweets 
at a specific day, groups tweets by countries in a specific days, finds out in what week day there were the majority
of tweets posted. There is a week_tweets_test.py, which is a testing module for week_tweets.py, that uses unittest to 
check a program working correctly.



