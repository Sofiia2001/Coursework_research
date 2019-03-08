import tweepy
from hidden import credentials
# hidden module cannot be posted on Github in terms of privacy policy

hidden_keys = credentials()
auth = tweepy.OAuthHandler(hidden_keys['CONSUMER_TOKEN'], hidden_keys['CONSUMER_SECRET'])
auth.set_access_token(hidden_keys['ACCESS_TOKEN'], hidden_keys['ACCESS_TOKEN_SECRET'])

api = tweepy.API(auth)
# '%23' is URL-encoded '#'
data = api.search('%23suicide')

# Prints out the user screenname of who posted this
# and a Tweet itself if data exists
if data:
    for post in data:
        print(post.user.screen_name)
        print(post.text)
        print(post.created_at)

        # Checks if there is a Tweet's location
        # If yes, prints country and a name of this place
        # In case of missing a place of a Tweet, it prints the location of a user
        if post.place:
            print(post.place.country)
            print(post.place.full_name)
        else:
            if post.user.location:
                print(post.user.location)
            else:
                print('No location is presented')

        print('\n')
else:
    print('Nobody has posted this')

