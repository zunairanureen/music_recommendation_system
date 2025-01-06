import pickle
import streamlit as st
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "25e11987b2f24a1395c529a3be48405d"
CLIENT_SECRET = "f14bdcd5f2904e6489e0f144d3811194"

# Spotify client setup
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = Spotify(client_credentials_manager=client_credentials_manager)

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    /* Entire app background and text styles */
    .stApp {
        background-color: #0d0d0d; /* Dark black background */
        color: #ffffff; /* White text for contrast */
        font-family: 'Arial', sans-serif; /* Clean font */
    }

    /* Title bar styling */
    header {
        background-color: #0d0d0d !important; /* Black background for the title bar */
        color: #ff0000 !important; /* Red title text */
        padding: 20px 0; /* Padding for the title */
        text-align: center;
    }

    /* Title text inside the header */
    header h1 {
        color: #ff0000; /* Red title text */
        font-size: 3rem; /* Larger text */
        text-shadow: 2px 2px 5px #660000; /* Red shadow effect */
    }

    /* Button styling */
    .stButton button {
        background-color: #ff0000; /* Red button */
        color: #ffffff; /* White text */
        border-radius: 12px; /* Rounded corners */
        border: 2px solid #ff0000; /* Solid red border */
        padding: 10px 20px;
    }

    .stButton button:hover {
        background-color: #b30000; /* Darker red on hover */
    }

    /* Dropdown styling */
    .stSelectbox div {
        background-color: #1a1a1a; /* Slightly lighter black for dropdown */
        color: #ffffff; /* White text */
    }

    /* Poster styling */
    img {
        border: 3px solid #ff0000; /* Red border around posters */
        border-radius: 10px; /* Rounded poster corners */
        width: 100%; /* Make images fit within columns */
        height: auto; /* Maintain aspect ratio */
    }

    /* Recommendation section text */
    .recommendation-text {
        color: #ff0000; /* Red text for song recommendations */
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to fetch album cover URL
def get_song_album_cover_url(song_name, artist_name):
    try:
        search_query = f"track:{song_name} artist:{artist_name}"
        search_results = sp.search(search_query, type="track", limit=1)
        if search_results["tracks"]["items"]:
            album_cover_url = search_results["tracks"]["items"][0]["album"]["images"][0]["url"]
            return album_cover_url
    except Exception as e:
        st.error(f"Error fetching album cover: {e}")
    return "https://via.placeholder.com/300?text=No+Image+Available"

# Function to recommend songs
def recommend(song):
    try:
        index = music[music['song'] == song].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_music_names = []
        recommended_music_posters = []

        for i in distances[1:6]:  # Recommend top 5 songs
            artist = music.iloc[i[0]]['artist']
            recommended_music_names.append(music.iloc[i[0]]['song'])
            poster_url = get_song_album_cover_url(music.iloc[i[0]]['song'], artist)
            recommended_music_posters.append(poster_url)

        return recommended_music_names, recommended_music_posters
    except IndexError:
        st.error("Selected song not found in the dataset.")
        return [], []
    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return [], []

# Streamlit app layout
st.title('🎶 Music Recommender System 🎵')

# Load preprocessed data
try:
    music = pickle.load(open('df', 'rb'))
    similarity = pickle.load(open('similar.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")

# Dropdown for song selection
song_list = music['song'].values if 'music' in locals() else []
selected_song = st.selectbox("Type or select a song from the dropdown", song_list)

# Display recommendations
if st.button('🎧 Show Recommendation 🎶'):
    if selected_song:
        recommended_song_names, recommended_song_posters = recommend(selected_song)

        # Display recommendations in columns
        if recommended_song_names:
            st.markdown("### Recommended Songs 🎤")
            cols = st.columns(5)  # Display 5 columns
            for idx, col in enumerate(cols):
                with col:
                    if idx < len(recommended_song_names):
                        st.markdown(f"**{recommended_song_names[idx]}**")
                        st.image(
                            recommended_song_posters[idx],
                            caption=recommended_song_names[idx],  # Add captions
                            use_container_width=True  # Make image fit within the container
                        )
    else:
        st.warning("Please select a song to get recommendations.")
