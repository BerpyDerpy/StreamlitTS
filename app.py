import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from io import BytesIO


def get_token():
    token = os.getenv("GENIUS_API_TOKEN")
    if not token:
        token = st.text_input(
            "Enter your Genius API Token:", type="password")
    return token


def search_songs(title, token):

    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": title}
    response = requests.get(f"{base_url}/search", headers=headers, params=params)
    data = response.json()
    hits = data.get("response", {}).get("hits", [])
    results = []
    for hit in hits:
        result = hit.get("result", {})
        song_title = result.get("title", "")
        artist = result.get("primary_artist", {}).get("name", "")
        path = result.get("path", "")
        results.append((song_title, artist, path))
    return results


def scrape_lyrics(song_url):

    page = requests.get(song_url)
    html = BeautifulSoup(page.text, "html.parser")

    lyrics_div = html.find("div", class_="Lyrics__Container")
    if lyrics_div:
        lyrics = lyrics_div.get_text(separator="\n")
    else:
        lyrics_divs = html.find_all("div", attrs={"data-lyrics-container": "true"})
        lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)
        if not lyrics:
            lyrics_divs = html.select('div[class^="Lyrics__Root"]')
            lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)

    return lyrics.strip()


def generate_wordcloud(text):

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white",
        collocations=False
    ).generate(text)
    return wc.to_image()


#  streamlit app

def main():
    st.title("Lyrics Explorer")
    st.write("Enter a Taylor Swift song title to fetch lyrics.")

    token = get_token()

    song_title = st.text_input("Song title", "Shake It Off")
    if st.button("Fetch Lyrics"):
        results = search_songs(song_title, token)

        if len(results) > 1:
            choices = [f"{title} — {artist}" for title, artist, _ in results]
            choice = st.selectbox("Select the correct song:", choices)
            idx = choices.index(choice)
        else:
            idx = 0

        song_path = results[idx][2]
        song_url = f"https://genius.com{song_path}"

        lyrics = scrape_lyrics(song_url)

        st.subheader("Lyrics")
        st.text_area("", lyrics, height=300)

        st.subheader("Word Cloud")
        wc_image = generate_wordcloud(lyrics)
        buf = BytesIO()
        wc_image.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Word Cloud of Lyrics", use_container_width=True)


if __name__ == "__main__":
    main()
