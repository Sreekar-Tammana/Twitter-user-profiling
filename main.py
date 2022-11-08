import configparser as cp
import pandas as pd
import streamlit as st
import tweepy as tp
import streamlit.components.v1 as components
from textblob import TextBlob
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import fun

# Read Configs
config = cp.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIf8gwEAAAAAPyF47sM6UGJKQGtVBcVL6t%2FVHwY%3DNciSlNBZEBq9heuovwgXXEKiX5la23y30inP1yNV6bMwIUT6oL'

# Authentication
auth = tp.OAuth1UserHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

# Instance of API
api = tp.API(auth, wait_on_rate_limit=True)



############################################################################
# STREAMLIT APP STARTS HERE......

# Title
st.title("Twitter User Profiling")
# st.title("Twitter User Profiling \U0001F923")

####
with st.form("my_form"):
    # st.write("Username")
    check_username = st.text_input("Username", key="name")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")


####################################################################
### TWEEPY
# # Enter Username (screen_name in tweepy)
name = check_username

no_of_tweets = st.slider('Select no. of tweets want to retrieve', 2, 25)

# # Getting User
# if name != "":
if name == "":
    pass
else:
    user = api.get_user(screen_name=name)
    data = user._json
    fun.basic_info(data)
    
    timeline = api.user_timeline(
        screen_name=name, count=200, include_rts=False, tweet_mode='extended')

    df = []
    display_df = []
    analysis = []
    analysis_emoji = []
    tweet_time = []
    days = []
    top_5_tweets = []
    likes = []
    links = []
    # tweet_id = {}

    for info in timeline:
        # print(info)
        # print('\n')
        df.append(info.full_text)
        analysis.append( TextBlob(info.full_text).sentiment.polarity )
        x = info.created_at
        tweet_time.append(x.strftime("%H"))
        days.append(x.strftime("%A"))
        likes.append(info.favorite_count)
        links.append(f"https://twitter.com/twitter/statuses/{info.id}")

    for info in timeline[:no_of_tweets]:
        display_df.append(info.full_text)
        # print(f"Created at : {info.created_at}\n")
        x = info.created_at
        # tweet_time.append(x.strftime("%H"))
        # days.append(x.strftime("%A"))
        # tweet_time.append(x.strftime("%I%p"))
    
    df_table = pd.DataFrame(data= df, columns= ['Tweets'])
    tweet_time_df = pd.DataFrame(data=tweet_time, columns=['Time'])
    tweet_time_df['Days'] = days
    df_table['Polarity'] = analysis
    # print(df_table['Polarity'].dtype)
    st.table(display_df)
    # st.table(links)
    # st.table(df_table)
    # fun.polarity_emojis(df_table['Polarity'], analysis_emoji)
    for val in analysis:
        if val >= -1 and val <= -0.6:
            analysis_emoji.append('😟')
        elif val >= -0.5 and val <= -0.1:
            analysis_emoji.append('😶')
        elif val == 0:
            analysis_emoji.append('😐')
        elif val >= 0.0 and val <= 0.4:
            analysis_emoji.append('🙂')
        elif val >= 0.4 and val <= 1:
            analysis_emoji.append('😀')


    # st.table(likes)
    df_table['Likes'] = likes
    df_table['Emoji'] = pd.DataFrame(analysis_emoji)
    st.table(df_table)

    most_liked_tweet = pd.DataFrame(data= links)
    # most_liked_tweet['Links'] = links
    most_liked_tweet['Likes'] = likes
    most_liked_tweet_df = most_liked_tweet.sort_values(by='Likes', ascending=False)
    st.table(most_liked_tweet_df)


    top_5_tweets_df = pd.DataFrame(data= top_5_tweets, columns=['Tweets', 'Likes'])
    top_5_tweets_df['Tweets'] = df_table['Tweets']
    top_5_tweets_df['Likes'] = likes
    st.table(top_5_tweets_df.sort_values(by='Likes', ascending=False))
    top_tweets_5 = top_5_tweets_df.sort_values(by='Likes', ascending=False)

    for t in top_tweets_5['Tweets'][:5]:
        print(t)

    ## Displaying top tweet
    st.title("Most liked tweet")
    class Tweet(object):
        def __init__(self, s, embed_str=False):
            if not embed_str:
                # Use Twitter's oEmbed API
                # https://dev.twitter.com/web/embedded-tweets
                api = "https://publish.twitter.com/oembed?url={}".format(s)
                response = requests.get(api)
                self.text = response.json()["html"]
            else:
                self.text = s

        def _repr_html_(self):
            return self.text

        def component(self):
            return components.html(self.text, height=600)

    t = Tweet(most_liked_tweet_df.iat[0, 0]).component()
    ## Displaying top tweet

    ### Download section
    tweet_time_df.to_csv(index=False)
    @st.experimental_memo
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(tweet_time_df)

    st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )
    ### Download section

    ### Chart display
    st.title("Activetly tweeted time")
    fig = tweet_time_df.set_index('Days')
    st._arrow_bar_chart(fig)
    ### Chart display
# print(data)

# if st.session_state.name != "":
    # st.title("Hi")
    # fun.basic_info(data)
    # st.caption("Username")
    # st.subheader(data['name'])
# else:
#     pass
    # st.session_state.name = ""
# else:
#     name = ""
# # print(type(user)) # CLASS type

# # Get particular data from "user" variable

# # Name of user
# print(f"Name : {data['name']}")
# if st.session_state.name != " ":
#     fun.display_name(data)
#     st.caption("Username")
#     st.subheader(data['name'])
# else:
#     st.session_state.name = ""

# # ID of user
# print(f"ID of {data['name']} : {data['id']}")

# Profile image of user
# print(f"Profile image : {data['profile_image_url']}")
# st.image(data['profile_image_url'])

# # Followers of user
# print(f"Followers : {user.followers_count}")

# # Friends of user
# print(f"Following : {data['friends_count']}")

# # Total number of tweets upto date
# print(f"Total number of tweets : {user.statuses_count}")

# # Getting user's tweets, time & day posted of every tweet
# timeline = api.user_timeline(
#     screen_name=name, count=200, include_rts=False, tweet_mode='extended')

# api.home_timeline
# print(timeline)
# df = []
# for info in timeline:
#     print('\n')
#     df.append(info.full_text)

    # print(ans['html'])
    # print(info)
    # print(f"ID of tweet {info.id}")
    # print(f"Created at : {info.created_at}")
    # x = info.created_at
    # print(f"Day created : {x.strftime('%a')}")
    # print(f'Time created : {x.strftime("%X")}')
    # print(f"Text of tweet : {info.full_text}")

# df_table = pd.DataFrame(data= df, columns= ['Tweets'])
# st.table(df_table)
