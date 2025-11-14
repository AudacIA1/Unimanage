# chatbot/training_data.py
"""
Contiene los datos de entrenamiento para el modelo de clasificación de intenciones de spaCy.

Este archivo define las frases de ejemplo para cada una de las intenciones que el
chatbot debe ser capaz de reconocer. La calidad y variedad de estos ejemplos son
cruciales para la precisión del modelo de NLP.

Para añadir una nueva intención:
1.  Añade el nombre de la nueva intención al diccionario `BASE_CATS`.
2.  Añade nuevos ejemplos a la lista `TRAIN_DATA` usando la función `create_training_example`.
"""

# Diccionario base para asegurar que todas las intenciones están presentes en cada
# ejemplo de entrenamiento, con una puntuación de 0.0 por defecto.
BASE_CATS = {
    "saludo": 0.0, 
    "despedida": 0.0, 
    "listar_activos_disponibles": 0.0, 
    "contar_activos_por_estado": 0.0, 
    "get_most_recent_loan": 0.0,
    "reportar_problema": 0.0,
    "afirmacion": 0.0,
    "negacion": 0.0,
    "listar_capacidades": 0.0
}

def create_training_example(text, intent):
    """
    Crea una tupla de datos de entrenamiento en el formato que spaCy espera.

    Args:
        text (str): La frase de ejemplo del usuario.
        intent (str): La intención asociada a esa frase.

    Returns:
        tuple: Una tupla que contiene el texto y un diccionario con la
               intención marcada con una puntuación de 1.0.
    """
    cats = BASE_CATS.copy()
    cats[intent] = 1.0
    return (text, {"cats": cats})

# Lista de todos los ejemplos de entrenamiento para el modelo de intenciones.
TRAIN_DATA = [
    # --- Intención: Saludar ---
    create_training_example("hola", "saludo"),
    create_training_example("buenos dias", "saludo"),
    create_training_example("buenas tardes", "saludo"),
    create_training_example("hey", "saludo"),
    create_training_example("que tal", "saludo"),
    create_training_example("saludos", "saludo"),
    create_training_example("hola chatbot", "saludo"),

    # --- Intención: Despedirse ---
    create_training_example("adios", "despedida"),
    create_training_example("hasta luego", "despedida"),
    create_training_example("chao", "despedida"),
    create_training_example("nos vemos", "despedida"),
    create_training_example("me voy", "despedida"),
    create_training_example("gracias, adios", "despedida"),

    # --- Intención: Listar activos disponibles ---
    create_training_example("muéstrame los activos disponibles", "listar_activos_disponibles"),
    create_training_example("qué equipos están libres", "listar_activos_disponibles"),
    create_training_example("ver los activos que se pueden usar", "listar_activos_disponibles"),
    create_training_example("dame la lista de recursos disponibles", "listar_activos_disponibles"),
    create_training_example("qué activos están libres ahora", "listar_activos_disponibles"),
    create_training_example("activos que puedo usar", "listar_activos_disponibles"),
    create_training_example("dame la lista de activos disponibles", "listar_activos_disponibles"),
    create_training_example("mostrar activos libres", "listar_activos_disponibles"),
    create_training_example("qué hay disponible", "listar_activos_disponibles"),

    # --- Intención: Contar activos por estado ---
    create_training_example("cuántos activos hay en mantenimiento", "contar_activos_por_estado"),
    create_training_example("dame el número de equipos en uso", "contar_activos_por_estado"),
    create_training_example("cantidad de activos disponibles", "contar_activos_por_estado"),
    create_training_example("cuántos están en mantenimiento", "contar_activos_por_estado"),
    create_training_example("cuántos activos hay en estado de uso", "contar_activos_por_estado"),
    create_training_example("dime cuántos equipos están disponibles", "contar_activos_por_estado"),
    create_training_example("número de activos en mantenimiento", "contar_activos_por_estado"),
    create_training_example("cuántos activos están en uso", "contar_activos_por_estado"),
    create_training_example("activos disponibles, cuántos son", "contar_activos_por_estado"),
    create_training_example("cuántos en uso", "contar_activos_por_estado"),
    create_training_example("dime la cantidad de activos en estado disponible", "contar_activos_por_estado"),

    # --- Intención: Obtener el préstamo más reciente ---
    create_training_example("cuál es el préstamo más reciente", "get_most_recent_loan"),
    create_training_example("dame el último préstamo", "get_most_recent_loan"),
    create_training_example("ver el préstamo más nuevo", "get_most_recent_loan"),
    create_training_example("último préstamo", "get_most_recent_loan"),
    create_training_example("quién pidió el último activo", "get_most_recent_loan"),
    create_training_example("dime el último activo prestado", "get_most_recent_loan"),
    create_training_example("préstamo reciente", "get_most_recent_loan"),

    # --- Intención: Reportar un problema ---
    create_training_example("quiero reportar un problema", "reportar_problema"),
    create_training_example("un equipo no funciona", "reportar_problema"),
    create_training_example("la laptop está rota", "reportar_problema"),
    create_training_example("el proyector tiene un fallo", "reportar_problema"),
    create_training_example("necesito ayuda con un activo", "reportar_problema"),
    create_training_example("tengo un problema con un activo", "reportar_problema"),
    create_training_example("necesito reportar una falla", "reportar_problema"),
    create_training_example("hay un equipo dañado", "reportar_problema"),
    create_training_example("el activo X no funciona", "reportar_problema"),
    create_training_example("reportar falla", "reportar_problema"),

    # --- Intención: Afirmación ---
    create_training_example("sí", "afirmacion"),
    create_training_example("si", "afirmacion"),
    create_training_example("claro", "afirmacion"),
    create_training_example("confirmo", "afirmacion"),
    create_training_example("acepto", "afirmacion"),
    create_training_example("dale", "afirmacion"),
    create_training_example("afirmativo", "afirmacion"),
    create_training_example("ok", "afirmacion"),

    # --- Intención: Negación ---
    create_training_example("no", "negacion"),
    create_training_example("cancela", "negacion"),
    create_training_example("no, gracias", "negacion"),
    create_training_example("para", "negacion"),
    create_training_example("cancelar", "negacion"),
    create_training_example("negativo", "negacion"),
    create_training_example("no quiero", "negacion"),

    # --- Intención: Listar capacidades ---
    create_training_example("qué puedes hacer", "listar_capacidades"),
    create_training_example("para qué sirves", "listar_capacidades"),
    create_training_example("cuáles son tus funciones", "listar_capacidades"),
    create_training_example("ayuda", "listar_capacidades"),
    create_training_example("qué sabes hacer", "listar_capacidades"),
    create_training_example("dime tus funciones", "listar_capacidades"),
    create_training_example("qué funcionalidades tienes", "listar_capacidades"),
    create_training_example("comandos", "listar_capacidades"),
    create_training_example("opciones", "listar_capacidades"),
]