from transformers import TapasTokenizer, TapasForQuestionAnswering
import torch

# Charger le modèle TAPAS et son tokenizer à partir des chemins locaux
model = TapasForQuestionAnswering.from_pretrained(r"C:\Users\Aycha\Desktop\stage\tapas_model")
tokenizer = TapasTokenizer.from_pretrained(r"C:\Users\Aycha\Desktop\stage\tapas_tokenizer")

# Fonction pour obtenir la réponse de TAPAS
def get_answer_from_tapas(df, question):
    df_copy = df.copy()
    df_copy = df_copy.astype(str)  # Convert all columns to strings
    inputs = tokenizer(table=df_copy, question=question, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)  # Get model outputs
    return tokenizer.decode(outputs.logits.argmax(dim=-1))  # Decode the answer
