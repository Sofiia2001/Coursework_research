import tweepy
from hidden import credentials # hidden module cannot be posted on Github in terms of privacy policy
import json
import csv
import time


def getting_data(consumer_token, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(hidden_keys['CONSUMER_TOKEN'], hidden_keys['CONSUMER_SECRET'])
    auth.set_access_token(hidden_keys['ACCESS_TOKEN'], hidden_keys['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    # '%23' is URL-encoded '#'
    data = api.search('%23suicide')
    return data


def forming_json(data):
    text_list = []
    text = ''
    dict_json = {} #dictionary to write into json file
    # Prints out the user screenname of who posted this
    # and a Tweet itself if data exists
    if data:
        for post in data:
            text += f'screen_name: {post.user.screen_name}'
            text += f'\ntext: {post.text}'
            text += f'\ncreated_at: {post.created_at}'
            dict_json['post {}'.format(data.index(post))] = {} #creates another sub-dict for every post
            dict_json['post {}'.format(data.index(post))]['screen_name'] = post.user.screen_name
            dict_json['post {}'.format(data.index(post))]['tweet_text'] = post.text
            dict_json['post {}'.format(data.index(post))]['created_at'] = str(post.created_at)


            # Checks if there is a Tweet's location
            # If yes, prints country and a name of this place
            # In case of missing a place of a Tweet, it prints the location of a user
            if post.place:
                text += f'\ncountry: {post.place.country}'
                text += f'\nfull_name: {post.place.full_name}'
                dict_json['post {}'.format(data.index(post))]['country_tweet'] = post.place.country
                dict_json['post {}'.format(data.index(post))]['full_place_name'] = post.place.full_name
            else:
                dict_json['post {}'.format(data.index(post))]['country_tweet'] = 'null'
                dict_json['post {}'.format(data.index(post))]['full_place_name'] = 'null'
                if post.user.location:
                    text += f'\nlocation: {post.user.location}'
                    dict_json['post {}'.format(data.index(post))]['user_location'] = post.user.location
                else:
                    dict_json['post {}'.format(data.index(post))]['user_location'] = 'null'
                    text += '\n' + 'location: No location is presented'
            text_list.append(text)
            text = ''

    return text_list


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


def writing_into_txt(consumer_token, consumer_secret, access_token, access_token_secret):
    text = []

    while True:
        data = getting_data(consumer_token, consumer_secret, access_token, access_token_secret)
        to_write = forming_json(data)

        for post in to_write:
            if post not in text:
                with open('testing_api.txt', 'a+') as txt_file:
                    if post not in txt_file.read():
                        txt_file.write(post + '\n' + '\n')
                text.append(post)
                print('Written!')
            else:
                print('Waiting for data to reload')

        time.sleep(60)



if __name__ == '__main__':
    hidden_keys = credentials()

    consumer_token = hidden_keys['CONSUMER_TOKEN']
    consumer_secret = hidden_keys['CONSUMER_SECRET']
    access_token = hidden_keys['ACCESS_TOKEN']
    access_token_secret = hidden_keys['ACCESS_TOKEN_SECRET']

    writing_into_txt(consumer_token, consumer_secret, access_token, access_token_secret)


