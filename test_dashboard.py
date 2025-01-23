import pytest
import pandas as pd
from unittest.mock import patch
from dashboard import display_sub_genre_graph, music_dashboard

def test_display_sub_genre_graph():
    # Exemple de données factices
    data = {
        'main_genre': ['Pop', 'Hip-Hop', 'Pop'],
        'track_genre': ['Pop-Rock', 'Rap', 'Electro-Pop'],
        'popularity': [90, 85, 75]
    }
    df = pd.DataFrame(data)
    selected_genre = 'Pop'

    # Vérifie que la fonction ne lève pas d'erreurs
    try:
        display_sub_genre_graph(df,selected_genre)
    except Exception as e:
        pytest.fail(f"Erreur inattendue : {e}")


def test_average_popularity():
    data = {
        'main_genre': ['Pop', 'Pop', 'Hip-Hop'],
        'popularity': [80, 90, 85]
    }
    df = pd.DataFrame(data)

    # Calcul attendu
    expected = {'Pop': 85, 'Hip-Hop': 85}
    actual = df.groupby('main_genre')['popularity'].mean().to_dict()

    assert actual == expected, f"Résultat incorrect : {actual}, attendu : {expected}"


@patch('streamlit.selectbox')
def test_user_interaction(mock_selectbox):
    # Simuler une sélection utilisateur
    mock_selectbox.return_value = 'Pop'
    result = mock_selectbox("Sélectionnez un genre principal", ['Pop', 'Hip-Hop'])
    
    assert result == 'Pop', "La sélection utilisateur n'est pas correcte."


