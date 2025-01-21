import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tapas_model import process_first_block

def music_dashboard(df):
    # Dashboard page
    st.title("🎵 Music Dashboard")
    st.subheader("Analyze music genres and characteristics to maximize sales!")

    # Visualization 1: Popularity by genre
    st.markdown("## Popularity by Genre")

    main_genre_popularity = df.groupby('main_genre')['popularity'].mean().sort_values(ascending=False)

    # Créer un graphique interactif avec Plotly pour les genres principaux
    fig = px.bar(
        main_genre_popularity,
        x=main_genre_popularity.index,
        y=main_genre_popularity.values,
        labels={'x': 'Genre', 'y': 'Popularity'},
        title='Popularity per Genre',
        color_discrete_sequence=['#008B8B'],  # Couleur pour les barres
    )

    # Afficher le graphique principal dans Streamlit
    st.plotly_chart(fig)

    # Ajouter un selectbox pour sélectionner un genre
    selected_genre = st.selectbox("Sélectionnez un genre principal pour voir les sous-genres", main_genre_popularity.index)

    # Fonction pour afficher les sous-genres en fonction du genre sélectionné
    def display_sub_genre_graph(selected_genre):
        # Filtrer les données pour le genre sélectionné
        filtered_df = df[df['main_genre'] == selected_genre]

        # Calculer la moyenne de la popularité par sous-genre
        avg_popularity = filtered_df.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).reset_index()

        # Créer un graphique des sous-genres pour le genre sélectionné
        fig_sub_genre = px.bar(
            avg_popularity,
            x='track_genre',
            y='popularity',
            labels={'track_genre': 'Sub-Genre', 'popularity': 'Average Popularity'},
            title=f'Average Popularity per Sub-genre for {selected_genre}',
            color_discrete_sequence=['#008B8B'],
        )
        st.plotly_chart(fig_sub_genre)

    # Afficher les sous-genres pour le genre sélectionné
    if selected_genre:
        display_sub_genre_graph(selected_genre)

    # Explication des résultats
    st.markdown(
        """
        **Interpretation:** Genres with higher average popularity are more likely to attract more listeners and maximize sales.
        """
    )

    # Visualization 2: Top artists by average popularity
    st.markdown("## Top Artists by Average Popularity")

    # Select the number of top artists to display
    top_n = st.selectbox(
        "Select the number of top artists to display:",
        options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],  # Options for the dropdown
        index=3  # Default to 5
    )

    # Data preparation
    top_artists = (
        df.groupby('artists')['popularity']
        .agg(['mean', 'count'])
        .sort_values(by='mean', ascending=False)
        .head(top_n)
    )

    # Plot top artists by popularity
    st.subheader(f"Top {top_n} Artists by Average Popularity")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_artists['mean'], y=top_artists.index, palette="viridis", ax=ax)

    # Add title and labels
    ax.set_title(f"Top {top_n} Artists by Average Popularity", fontsize=16, weight='bold')
    ax.set_xlabel("Average Popularity", fontsize=12)
    ax.set_ylabel("Artists", fontsize=12)
    sns.despine(left=True, bottom=True)

    # Display the plot
    st.pyplot(fig)

    # Artist selection dropdown
    st.markdown("### Select an Artist to See Why They Are the Best")
    artist_options = top_artists.index.tolist()
    selected_artist = st.selectbox("Choose an artist", artist_options)

    # Filter data for the selected artist
    artist_data = df[df['artists'] == selected_artist]

    # Display analysis for the selected artist based on track attributes
    st.markdown(f"### Analysis for {selected_artist}")

    # Attributes to analyze: energy, key, loudness, mode, speechiness, etc.
    attributes = ['energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo']

    # Show analysis for each attribute
    attribute_data = {
        'Attribute': [],
        'Average Value': [],
    }

    # Calculate the average value for each attribute
    for attribute in attributes:
        mean_value = artist_data[attribute].mean()
        attribute_data['Attribute'].append(attribute.capitalize())
        attribute_data['Average Value'].append(f"{mean_value:.2f}")

    # Convert to a DataFrame
    attribute_df = pd.DataFrame(attribute_data)

    # Display the table
    st.table(attribute_df)

    # Provide some interpretation based on the attribute (general interpretation)
    st.markdown(
        """
        **Interpretation:** The combination of these musical features helps define the unique style of an artist. Artists who excel in energy, loudness, and valence are likely to produce tracks that resonate well with a wide audience, boosting their popularity and success.
        """
    )


    # Visualization 3: Track features by genre
    st.markdown("## Track Features by Genre")
    col1, col2 = st.columns(2)

    with col1:
        # Sélectionner les genres
        genres = df["track_genre"].unique()
        selected_genres = st.multiselect("Select genres", genres, default=genres[:3])

    with col2:
        # Sélectionner une fonctionnalité à afficher
        feature = st.selectbox("Select a feature", ["danceability", "energy", "tempo", "valence"])

    # Filtrer les données en fonction des genres sélectionnés
    filtered_data = df[df["track_genre"].isin(selected_genres)]

    # Calculer la moyenne de la fonctionnalité par genre
    feature_data = filtered_data.groupby("track_genre")[feature].mean().reset_index()

    fig2 = px.bar(
        feature_data,
        x="track_genre",
        y=feature,
        title=f"Average {feature.capitalize()} by Genre",
        labels={feature: feature.capitalize(), "track_genre": "Genre"},
        color_discrete_sequence=['#008B8B']
    )
    fig2.update_traces(
        texttemplate='%{y}',  # Afficher la valeur de 'y' (la moyenne de la fonctionnalité)
        textposition= 'outside',  # Positionner le texte à l'extérieur des barres
    )
    # Modifier les axes pour enlever l'échelle de l'axe Y
    fig2.update_layout(
        yaxis=dict(showticklabels=False, showgrid=False,),  # Supprimer les ticks de l'axe Y
        xaxis_title=None,  # Supprimer le titre de l'axe X
        yaxis_title=None,  # Supprimer le titre de l'axe Y
        margin=dict(l=50, r=50, t=50, b=50),  # Ajuster les marges pour une meilleure lisibilité
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig2)

    # Add TAPAS question answering functionality
    st.markdown("## Ask a Question")
    question = st.text_input("What would you like to know about the music data?")
    if question:
        st.markdown(f"**Question  :** {question}")
        answer = process_first_block(df.astype(str), question, max_rows=256)
        st.markdown(f"**answer :** {answer}")
