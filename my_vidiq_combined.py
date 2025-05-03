
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
import time

st.set_page_config(page_title="My vidIQ – All-in-One", layout="centered")
st.title("🎯 My vidIQ – YouTube Keyword & Tag Generator")

keyword = st.text_input("Enter your video topic or keyword:")

def fetch_youtube_autosuggest(query):
    url = "https://suggestqueries.google.com/complete/search"
    params = {"client": "firefox", "ds": "yt", "q": query}
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()[1]
    except:
        pass
    return []

def get_search_volume(term):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([term], cat=0, timeframe='today 12-m', geo='', gprop='youtube')
        df = pytrends.interest_over_time()
        if not df.empty:
            return round(df[term].mean(), 2)
    except:
        pass
    return 0

def get_competition(keyword):
    try:
        url = f"https://www.youtube.com/results?search_query={keyword}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            return len(soup.find_all("ytd-video-renderer"))
    except:
        pass
    return 1

def calculate_score(volume, competition):
    return round((volume / competition) * 100, 2) if competition else round(volume * 100, 2)

def get_trending_tags(base_keyword):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([base_keyword], cat=0, timeframe='today 12-m', geo='', gprop='youtube')
        related = pytrends.related_queries()[base_keyword]['top']
        if related is not None:
            return related['query'].tolist()
    except:
        pass
    return []

if keyword:
    with st.spinner("🔍 Fetching suggestions, analyzing trends, and generating tags..."):
        autosuggest = fetch_youtube_autosuggest(keyword)
        trend_tags = get_trending_tags(keyword)
        all_keywords = list(set(autosuggest + trend_tags))

        results = []
        for key in all_keywords:
            vol = get_search_volume(key)
            comp = get_competition(key)
            score = calculate_score(vol, comp)
            results.append({"Keyword": key, "Search Volume": vol, "Competition": comp, "Score": score})
            time.sleep(1)

        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)
        top_tags = df["Keyword"].tolist()[:24]
        tag_string = ", ".join(top_tags)

        st.subheader("📊 Keyword Suggestions")
        st.dataframe(df)
        st.download_button("📥 Download CSV", df.to_csv(index=False), file_name="vidiq_keywords.csv")
        st.download_button("⬇️ Download Tags as TXT", tag_string, file_name=f"{keyword}_tags.txt")

        st.subheader("🔖 YouTube Tags")
        st.code(tag_string, language="text")
