import twitter
import _privatekeys

api = twitter.Api(consumer_key=_privatekeys.twitterConsumerKey,
                  consumer_secret=_privatekeys.twitterConsumerSecret,
                  access_token_key=_privatekeys.twitterAccessToken,
                  access_token_secret=_privatekeys.twitterAccessTokenSecret)

print(api.VerifyCredentials())

# statuses = api.GetUserTimeline(screen_name=user)
statuses = api.GetMentions()
for s in statuses:
    # behöver tidpunkt, hasha tidpunkt och meddelande till logg över vad som gjorts
    # leta upp namnet så det går att svara
    # ha hashtag för att skilja ut länkar som ska testas från paper.li och annan skit i mentions
    # har BeautifulSoup kod för att hitta URLar?
    # print(s.text)
    try:
        print('Tweet: {0}\nPublished: {1}'.format(s.text, s.created_at))
    # {"created_at": "Tue Jun 15 16:30:41 +0000 2010", "description": "Helping web professionals with #webperf and #webanalytics since 2010.", "favourites_count": 109, "followers_count": 482, "friends_count": 1156, "id": 155955796, "lang": "en", "listed_count": 84, "location": "Gothenburg, Sweden", "name": "Web Analytics Today", "profile_background_color": "000000", "profile_background_image_url": "http://abs.twimg.com/images/themes/theme5/bg.gif", "profile_banner_url": "https://pbs.twimg.com/profile_banners/155955796/1453460635", "profile_image_url": "http://pbs.twimg.com/profile_images/781948051330048002/c7z7T88b_normal.jpg", "profile_link_color": "487680", "profile_sidebar_fill_color": "000000", "profile_text_color": "000000", "screen_name": "AnalyticsCrew", "status": {"created_at": "Fri Apr 28 22:01:19 +0000 2017", "id": 858078701896052736, "id_str": "858078701896052736", "lang": "en", "source": "<a href=\"http://verifierad.nu\" rel=\"nofollow\">Analytics Crew</a>", "text": "Testing 1-2-3!"}, "statuses_count": 1182, "time_zone": "Stockholm", "url": "https://t.co/Zlyc8qZT6x", "utc_offset": 7200}
    except:
        print('Crap!')

# status = api.PostUpdate('Testing 1-2-3!')
# print(status.text)
