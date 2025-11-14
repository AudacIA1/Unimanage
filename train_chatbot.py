# train_chatbot.py
import spacy
import random
from spacy.training.example import Example
from apps.chatbot.training_data import TRAIN_DATA
import pathlib

def train_spacy_model(data, iterations=20, model_output_dir='chatbot_model'):
    """Entrena un nuevo modelo de clasificación de texto de spaCy."""
    # Crear un modelo en blanco para el idioma español
    nlp = spacy.blank("es")

    # Añadir el clasificador de texto al pipeline
    textcat = nlp.add_pipe("textcat")

    # Añadir las etiquetas (nombres de las intenciones) al clasificador
    labels = ["saludo", "despedida", "listar_activos_disponibles", "contar_activos_por_estado", "get_most_recent_loan", "reportar_problema", "afirmacion", "negacion", "listar_capacidades"]
    for label in labels:
        textcat.add_label(label)

    # Iniciar el entrenamiento
    optimizer = nlp.begin_training()
    print("Iniciando entrenamiento...")

    for i in range(iterations):
        random.shuffle(data)
        losses = {}
        for text, annotations in data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer, drop=0.35, losses=losses)
        print(f"Iteración {i+1}/{iterations}, Pérdida: {losses['textcat']:.4f}")

    # Guardar el modelo entrenado en un directorio
    output_dir = pathlib.Path(model_output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print(f"\nModelo guardado en: {output_dir}")

if __name__ == "__main__":
    train_spacy_model(TRAIN_DATA)
