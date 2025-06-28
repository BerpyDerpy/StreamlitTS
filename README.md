#  Lyrics Explorer

A simple Streamlit application that allows you to search for Taylor Swift songs on Genius.com, retrieve their lyrics, and visualize the most frequent words in a word cloud.

## Features

  * **Search Songs:** Find Taylor Swift songs using the Genius API.
  * **Fetch Lyrics:** Scrape full lyrics directly from Genius.com song pages.
  * **Word Cloud Visualization:** Generate and display a word cloud based on the fetched lyrics.
  * **API Token Handling:** Securely handle your Genius API token via environment variables or direct input.

## Prerequisites

**Install the required Python packages:**

    
    pip install streamlit requests beautifulsoup4 wordcloud
    

## Getting a Genius API Token

To use this application, you need a Client Access Token from the Genius API.

1.  Go to the Genius Developers website: [https://genius.com/developers](https://genius.com/developers)
2.  Sign in with your Genius account (or create one).
3.  Click "New API Client" (or similar).
4.  Fill in the required information. For "Redirect URI", you can use `http://localhost:8501` as a placeholder for this local application.
5.  After creating the client, you will see your "Client Access Token". Copy this token.

## How to Run


1.  **Run the Streamlit application:**
    Ensure your virtual environment is active (if you created one).

    ```bash
    streamlit run app.py
    ```

3.  Your web browser should automatically open to the Streamlit application (usually at `http://localhost:8501`).

## Usage

1.  Enter your Genius API Token into the provided input field.
2.  Type the name of a Taylor Swift song (e.g., "All Too Well", "Shake It Off") into the "Song title" text box.
3.  Click the "Fetch Lyrics" button.
4.  If multiple songs match, select the correct one from the dropdown menu.
5.  The lyrics will be displayed, followed by a word cloud visualization.
