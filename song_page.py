import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.io as pio
# Load data (replace 'dataset.csv' with the actual path to your data file)
@st.cache_data
def load_data():
    df = pd.read_csv('dataset.csv')  # Replace with the path to your CSV file
    df['popularity'] = df['popularity'] / 100
    return df

# Function to display song analysis
def song_analysis(song):
    # Display basic song information

    # Display loudness and tempo with a comment based on their values
    loudness = song['loudness']
    tempo = song['tempo']
    
    # Comment for loudness based on value
    if loudness > -5:
        loudness_comment = "Very Loud"
    elif loudness > -10:
        loudness_comment = "Moderately Loud"
    else:
        loudness_comment = "Soft"
    
    # Comment for tempo based on value
    if tempo > 120:
        tempo_comment = "Fast Tempo"
    elif tempo > 80:
        tempo_comment = "Moderate Tempo"
    else:
        tempo_comment = "Slow Tempo"
    
    # Display loudness and tempo with their comments
    st.write(f"**Loudness**: {loudness} dB ({loudness_comment})")
    st.write(f"**Tempo**: {tempo} BPM ({tempo_comment})")
    
    # Features to visualize
    features = ['danceability', 'energy', 'speechiness', 'acousticness', 
                'instrumentalness', 'liveness', 'valence', 'popularity']
    
    # Prepare the data for the bar plot
    feature_values = [song[feature] for feature in features]

    fig3 = go.Figure(data=[go.Bar(
        x=features,
        y=feature_values,
        text=feature_values,  # Afficher les valeurs de 'y' en tant que texte
        texttemplate='%{text:.2f}',  # Afficher la valeur avec deux décimales
        textposition='outside',  # Positionner le texte à l'extérieur des barres
    )])

    # Personnaliser le graphique
    fig3.update_layout(
        title='Song Feature Analysis',
        xaxis_title='Feature',
        yaxis_title='',  # Enlever le titre de l'axe y
        yaxis=dict(showticklabels=False),  # Masquer les ticks de l'axe y
        xaxis_tickangle=45,  # Rotation des labels de l'axe x
    )

    # Afficher le graphique
    st.plotly_chart(fig3)
