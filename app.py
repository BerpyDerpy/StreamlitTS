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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        page = requests.get(song_url, headers=headers)
        page.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error fetching lyrics: {e}. Status code: {page.status_code}")  # Show status code
        return ""
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to Genius website: {e}")
        return ""

    html = BeautifulSoup(page.text, "html.parser")

    lyrics_div = html.find("div", class_="Lyrics__Container")
    if lyrics_div:
        lyrics = lyrics_div.get_text(separator="\n")
    else:
        lyrics_divs = html.find_all("div", attrs={"data-lyrics-container": "true"})
        lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)
        if not lyrics:
            # Another common pattern for lyrics sections
            lyrics_divs = html.select('div[class^="Lyrics__Root"]')
            lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)

    # Add a debug print/log to see what lyrics are being scraped in deployment
    if not lyrics.strip():  # Check if it's truly empty after stripping
        st.warning(
            f"No lyrics scraped for {song_url}. HTML content snippet: {page.text[:500]}")  # Print first 500 chars of HTML

    return lyrics.strip()





def generate_wordcloud(text):
    if not text:
        return None  # Return None or an empty image if text is empty
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
        if not lyrics:
            st.error(
                "Could not retrieve lyrics for the selected song. The website structure might have changed, or there might be an issue with the song page itself.")
            # Do not attempt to generate word cloud if lyrics are empty
            return

        st.subheader("Lyrics")
        st.text_area("", lyrics, height=300)

        st.subheader("Word Cloud")
        wc_image = generate_wordcloud(lyrics)
        buf = BytesIO()
        wc_image.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Word Cloud of Lyrics", use_container_width=True)


if __name__ == "__main__":
    main()
