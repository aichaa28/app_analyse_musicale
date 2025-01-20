import streamlit as st
import pandas as pd
from dashboard import dashboard
from home_page import home_page
from song_page import song_analysis

# Charger les données
@st.cache_data
def load_data():
    return pd.read_csv('dataset.csv')  # Remplacez par le chemin de votre fichier CSV


st.title("🎵 Welcome to the Music Dashboard")
st.subheader("Explore the characteristics of songs and music genres.")

tabs = st.tabs(["Home", "Dashboard", "Song Analysis"])

# Afficher le contenu pour chaque onglet
with tabs[0]:
    home_page()

with tabs[1]:
    st.header("Dashboard")
    st.write("This section shows an overview of the data and metrics related to the music app.")
    df = load_data()  # Charger les données lorsque la page de dashboard est ouverte
    dashboard(df)

with tabs[2]:
    st.title("Select a Song for Analysis")

    # Song selection dropdown
    song_list = df[['track_name', 'artists']].drop_duplicates()
    song_options = song_list['track_name'] + " - " + song_list['artists']
    selected_song = st.selectbox("Choose a song", song_options)
    df['popularity'] = df['popularity'] / 100
    # Get the data for the selected song
    song = df[df['track_name'] == selected_song.split(" - ")[0]].iloc[0]

    # Show the analysis for the selected song
    song_analysis(song)
