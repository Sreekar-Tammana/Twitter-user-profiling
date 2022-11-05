import configparser as cp
import pandas as pd
import streamlit as st
import tweepy as tp
import streamlit.components.v1 as components
from textblob import TextBlob
import matplotlib.pyplot as plt
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
    # tweet_id = {}

    for info in timeline[:2]:
        # print(info)
        # print('\n')
        df.append(info.full_text)
        analysis.append( TextBlob(info.full_text).sentiment.polarity )

    for info in timeline[:no_of_tweets]:
        display_df.append(info.full_text)
    
    df_table = pd.DataFrame(data= df, columns= ['Tweets'])
    df_table['Polarity'] = analysis
    st.table(display_df)

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
