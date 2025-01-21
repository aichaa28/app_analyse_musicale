import pandas as pd
from transformers import TapasTokenizer, TapasForQuestionAnswering
import torch

model = TapasForQuestionAnswering.from_pretrained(r"C:\Users\Aycha\Desktop\stage\tapas_model")
tokenizer = TapasTokenizer.from_pretrained(r"C:\Users\Aycha\Desktop\stage\tapas_tokenizer")

def get_answer_from_tapas(df, question):
    if not question.strip():
        raise ValueError("La question ne peut pas être vide.")
    
    # Convertir toutes les colonnes en chaînes de caractères
    df = df.astype(str)
    
    # Préparer les entrées pour le modèle
    inputs = tokenizer(table=df, queries=[question], return_tensors="pt", padding="max_length", truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extraire les logits et effectuer le traitement correct
    logits = outputs.logits

    # Logits contiennent les prédictions sous forme d'un tableau
    predicted_index = logits.argmax(dim=-1).item()  # Obtenir l'indice de la réponse

    # Si nous avons une réponse, elle doit être sous forme de coordonnée
    if predicted_index == 0:
        return "Aucune réponse trouvée."
    else:
        # Extraire la réponse en utilisant les coordonnées
        row, col = predicted_index // df.shape[1], predicted_index % df.shape[1]
        
        if row < df.shape[0] and col < df.shape[1]:
            return df.iloc[row, col]
        else:
            return "Coordonnée hors limites."

# Fonction pour traiter uniquement le premier bloc d'un DataFrame
def process_first_block(df, question, max_rows=256):
    """
    Traite uniquement le premier bloc d'un DataFrame.
    """
    # Vérifier si le DataFrame est plus grand que max_rows
    if len(df) > max_rows:
        print(f"La table contient {len(df)} lignes. Utilisation des {max_rows} premières lignes.")
        df = df.iloc[:max_rows]
    
    # Obtenir la réponse pour le premier bloc
    try:
        answer = get_answer_from_tapas(df, question)
    except Exception as e:
        answer = f"Erreur : {str(e)}"
    
    return answer