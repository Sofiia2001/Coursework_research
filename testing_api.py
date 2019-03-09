import tweepy
from hidden import credentials # hidden module cannot be posted on Github in terms of privacy policy
import json
import csv
# from bs4 import BeautifulSoup
# Work with beautifulsoup will be posted later


def getting_data(consumer_token, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(hidden_keys['CONSUMER_TOKEN'], hidden_keys['CONSUMER_SECRET'])
    auth.set_access_token(hidden_keys['ACCESS_TOKEN'], hidden_keys['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    # '%23' is URL-encoded '#'
    data = api.search('%23suicide')
    return data


def forming_json(data):
    dict_json = {} #dictionary to write into json file
    # Prints out the user screenname of who posted this
    # and a Tweet itself if data exists
    if data:
        for post in data:
            print(post.user.screen_name)
            print(post.text)
            print(post.created_at)
            dict_json['post {}'.format(data.index(post))] = {} #creates another sub-dict for every post
            dict_json['post {}'.format(data.index(post))]['screen_name'] = post.user.screen_name
            dict_json['post {}'.format(data.index(post))]['tweet_text'] = post.text
            dict_json['post {}'.format(data.index(post))]['created_at'] = str(post.created_at)


            # Checks if there is a Tweet's location
            # If yes, prints country and a name of this place
            # In case of missing a place of a Tweet, it prints the location of a user
            if post.place:
                print(post.place.country)
                print(post.place.full_name)
                dict_json['post {}'.format(data.index(post))]['country_tweet'] = post.place.country
                dict_json['post {}'.format(data.index(post))]['full_place_name'] = post.place.full_name
            else:
                dict_json['post {}'.format(data.index(post))]['country_tweet'] = 'null'
                dict_json['post {}'.format(data.index(post))]['full_place_name'] = 'null'
                if post.user.location:
                    print(post.user.location)
                    dict_json['post {}'.format(data.index(post))]['user_location'] = post.user.location
                else:
                    dict_json['post {}'.format(data.index(post))]['user_location'] = 'null'
                    print('No location is presented')

            print('\n')
    else:
        print('Nobody has posted this')

    return dict_json


def write_into_json(dict_json):
    with open('testing_api.json', 'w', encoding = 'utf-8') as file:
        json.dump(dict_json, file, ensure_ascii = False)



def write_into_csv(dict_json):
    with open('testing_api.csv', mode = 'w') as csv_file:

        fieldnames = ['screen_name', 'tweet_text', 'created_at',
                      'country_tweet', 'full_place_name', 'user_location']
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        writer.writeheader()

        for post in dict_json:
            writer.writerow(dict_json[post])



if __name__ == '__main__':
    hidden_keys = credentials()

    consumer_token = hidden_keys['CONSUMER_TOKEN']
    consumer_secret = hidden_keys['CONSUMER_SECRET']
    access_token = hidden_keys['ACCESS_TOKEN']
    access_token_secret = hidden_keys['ACCESS_TOKEN_SECRET']

    data = getting_data(consumer_token, consumer_secret, access_token, access_token_secret)
    dict_json = forming_json(data)
    write_into_json(dict_json)
    write_into_csv(dict_json)

