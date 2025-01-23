import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tapas_model_code import process_first_block


# Fonction pour afficher la popularité par genre
def plot_genre_popularity(df):
    st.markdown("## Popularity by Genre")
    main_genre_popularity = df.groupby('main_genre')['popularity'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        main_genre_popularity,
        x=main_genre_popularity.index,
        y=main_genre_popularity.values,
        labels={'x': 'Genre', 'y': 'Popularity'},
        title='Popularity per Genre',
        color_discrete_sequence=['#008B8B']
    )
    st.plotly_chart(fig)

    st.markdown(
        """
        **Interpretation:** Pop and Hip-hop/Rap are the most popular genres, each representing over 40% of the total popularity.
        These genres likely attract the largest audiences.
        """
    )


# Fonction pour afficher les sous-genres d'un genre principal
def display_sub_genre_graph(df, selected_genre):
    filtered_df = df[df['main_genre'] == selected_genre]
    avg_popularity = filtered_df.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).reset_index()

    fig_sub_genre = px.bar(
        avg_popularity,
        x='track_genre',
        y='popularity',
        labels={'track_genre': 'Sub-Genre', 'popularity': 'Average Popularity'},
        title=f'Average Popularity per Sub-genre for {selected_genre}',
        color_discrete_sequence=['#008B8B'],
    )
    st.plotly_chart(fig_sub_genre)


# Fonction pour afficher les artistes les plus populaires
def plot_top_artists(df):
    st.markdown("## Top Artists by Average Popularity")
    top_n = st.selectbox("Select the number of top artists to display:", options=[2, 3, 5, 10, 15, 20], index=2)

    top_artists = (
        df.groupby('artists')['popularity']
        .agg(['mean', 'count'])
        .sort_values(by='mean', ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_artists['mean'], y=top_artists.index, palette="viridis", ax=ax)
    ax.set_title(f"Top {top_n} Artists by Average Popularity", fontsize=16, weight='bold')
    ax.set_xlabel("Average Popularity", fontsize=12)
    ax.set_ylabel("Artists", fontsize=12)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig)

    selected_artist = st.selectbox("Choose an artist", top_artists.index.tolist())
    display_artist_analysis(df, selected_artist)


# Fonction pour analyser un artiste sélectionné
def display_artist_analysis(df, selected_artist):
    st.markdown(f"### Analysis for {selected_artist}")
    artist_data = df[df['artists'] == selected_artist]

    attributes = ['energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo']
    attribute_data = {
        'Attribute': [attr.capitalize() for attr in attributes],
        'Average Value': [f"{artist_data[attr].mean():.2f}" for attr in attributes]
    }

    st.table(pd.DataFrame(attribute_data))

    st.markdown(
        """
        **Interpretation:** These musical attributes define the artist's style. For instance, high energy and loudness
        often correlate with tracks that engage a wide audience.
        """
    )


# Fonction pour afficher les fonctionnalités des pistes par genre
def plot_track_features_by_genre(df):
    st.markdown("## Track Features by Genre")
    col1, col2 = st.columns(2)

    with col1:
        genres = df["track_genre"].unique()
        selected_genres = st.multiselect("Select genres", genres, default=genres[:3])

    with col2:
        feature = st.selectbox("Select a feature", ["danceability", "energy", "tempo", "valence"])

    filtered_data = df[df["track_genre"].isin(selected_genres)]
    feature_data = filtered_data.groupby("track_genre")[feature].mean().reset_index()

    fig2 = px.bar(
        feature_data,
        x="track_genre",
        y=feature,
        title=f"Average {feature.capitalize()} by Genre",
        labels={feature: feature.capitalize(), "track_genre": "Genre"},
        color_discrete_sequence=['#008B8B']
    )
    st.plotly_chart(fig2)


# Fonction pour traiter les questions TAPAS
def tapas_question_answering(df):
    st.markdown("## Ask a Question")
    question = st.text_input("What would you like to know about the music data?")
    if question:
        st.markdown(f"**Question:** {question}")
        answer = process_first_block(df.astype(str), question, max_rows=256)
        st.markdown(f"**Answer:** {answer}")


# Fonction principale du tableau de bord
def music_dashboard(df):
    st.title("🎵 Music Dashboard")
    st.subheader("Analyze music genres and characteristics to maximize sales!")

    plot_genre_popularity(df)

    selected_genre = st.selectbox("Select a main genre to see sub-genres", df['main_genre'].unique())
    if selected_genre:
        display_sub_genre_graph(df, selected_genre)

    plot_top_artists(df)
    plot_track_features_by_genre(df)
    tapas_question_answering(df)
