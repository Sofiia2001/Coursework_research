import sqlite3
import datetime
from tqdm import tqdm
import geocoder


class WeekTweets:
    def __init__(self):
        '''
        Asks user to input a date of a week to form a whole week
        '''
        self.date = ''
        self._week_list = []
        self._tweets_week_dict = {}
        self.num_of_tweets = {}

    def select_week(self):
        '''
        Creates a week due to a correct calendar

        :return: None
        '''
        self.date = input('Enter the date [dd.mm]: ')
        assert 0 < int(self.date[:2]) <= 31, 'Date is not correct'
        assert 0 < int(self.date[3:]) <= 12, 'Date is not correct'

        date = datetime.datetime(2019, int(self.date[3:]), int(self.date[:2]))
        for i in range(date.weekday(), 0, -1):
            self._week_list.append((date - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
        self._week_list.append(date.strftime('%Y-%m-%d'))
        for j in range(1, 7 - date.weekday()):
            self._week_list.append((date + datetime.timedelta(days=j)).strftime('%Y-%m-%d'))

    def tweets_for_week(self):
        '''
        Collects all the tweets from a gathered database in weekdays formed before

        :return: dictionary with date: tweets made in that day
        '''
        self.select_week()
        with sqlite3.connect('Twitter_data.db') as connection:
            cursor = connection.cursor()

            for w in self._week_list:

                select = "SELECT * FROM TWITTER WHERE created_at LIKE ?"

                cursor.execute(select, [(f'%{w}%')])
                res = cursor.fetchall()
                self._tweets_week_dict[w] = len(res)

    def find_week_day(self):
        '''
        Finds week day when the biggest number of tweets was posted

        :return: max week day of a week
        '''
        maxx = max(self._tweets_week_dict.values())
        for i in self._tweets_week_dict:
            if self._tweets_week_dict[i] == maxx:
                key = i.split('-')
                date = datetime.datetime(int(key[0]), int(key[1]), int(key[2]))
        return date.strftime('%A')

    def tweets_for_week_day(self):
        '''
        Returns number of tweets on a certain day from different countries

        :return: amount of tweets on mondays(eg)
        '''
        # day = input('Please, choose a week day you want to analyze\n'
                    # '[mon/tue/wed/thu/fri/sat/sun]: ')

        weekdays = {
            'mon': 'Monday',
            'tue': 'Tuesday',
            'wed': 'Wednesday',
            'thu': 'Thursday',
            'fri': 'Friday',
            'sat': 'Saturday',
            'sun': 'Sunday'
        }

        self.num_of_tweets = {v: {'general': 0, 'dates': set(), 'posts': {}} for v in weekdays.values()}

        with sqlite3.connect('Twitter_data.db') as connection:
            cursor = connection.cursor()

            select = "SELECT created_at FROM TWITTER"
            cursor.execute(select)
            res = cursor.fetchall()

            res = [date[0].replace(': ', '').strip() for date in res]
            for date in res:
                d = date[:date.index(' ')]
                splitted = d.split('-')
                day = datetime.datetime(int(splitted[0]), int(splitted[1]), int(splitted[2])).strftime('%A')

                if day in self.num_of_tweets:
                    self.num_of_tweets[day]['general'] += 1
                    self.num_of_tweets[day]['dates'].add(d)

            user_day = 'Monday' #only as example
            locations = []
            countries = {}
            for u_date in self.num_of_tweets[user_day]['dates']:
                selection = "SELECT * FROM TWITTER WHERE created_at LIKE ?"
                cr_at = f'%{u_date}%'
                cursor.execute(selection, [(cr_at)])

                posts = cursor.fetchall()
                for p in posts:
                    if 'No location' not in p[3]: locations.append(p[3].replace(': ', '').strip())

                self.num_of_tweets[user_day]['posts'][u_date] = posts


            with sqlite3.connect('Cities_data.db') as connect:
                for loc in locations:
                    if ',' in loc: loc = loc[:loc.index(',')]
                    cursor_1 = connect.cursor()

                    select = "SELECT country_name FROM CITIES WHERE city=?"
                    cursor_1.execute(select, [(loc)])
                    print(loc)
                    res = cursor.fetchall()
                    # print(res)

                    try:
                        geo = geocoder.geonames(loc, key='sofiiatatosh')
                        country = geo.country
                    except:
                        country = res[0][0]

                    countries[country] = countries.get(country, 0)
                    countries[country] += 1

        return countries
