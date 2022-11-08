import streamlit as st
import requests as rq

# Removes '_normal' from image link, so image resolution increases :)
def remove_normal(link):
    return link.replace('_normal', '')

def basic_info(data):
    st.header(data['name'])
    re_link = remove_normal(data['profile_image_url'])
    st.image(re_link, width=200)
    st.markdown(f"#### ID : {data['id']} ")
    st.markdown(f"#### Followers : {data['followers_count']}")
    st.markdown(f"#### Following : {data['friends_count']}")
    st.markdown(f"#### Total number of tweets (Till date) : {data['statuses_count']}")

def tweet_url(s_name, t_id):
    input_url = f"https://twitter.com/{s_name}/status/{t_id}"
    api = "https://publish.twitter.com/oembed?url={}".format(input_url)
    response = rq.get(api)
    res = response.json()
    return res

def polarity_emojis(dataframe, df_store):
    for val in range(dataframe):
        if val >= -1 and val <= -0.6:
            df_store.append('😟')
        elif val >= -0.5 and val <= -0.1:
            df_store.append('😶')
        elif val >= 0.0 and val <= 0.1:
            df_store.append('😐')
        elif val >= 0.2 and val <= 0.6:
            df_store.append('🙂')
        elif val >= 0.5 and val <= 1:
            df_store.append('😀')