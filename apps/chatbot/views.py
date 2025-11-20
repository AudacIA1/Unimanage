# chatbot/views.py
import spacy
from django.http import JsonResponse
import json
from .tools import get_available_assets, count_assets_by_status, get_most_recent_loan, create_maintenance_request
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# --- Carga de Modelos de spaCy ---
# Se cargan los modelos de NLP al iniciar el servidor para un rendimiento óptimo.
# nlp_intent: Modelo personalizado para la clasificación de intenciones.
# nlp_ner: Modelo pre-entrenado de spaCy para el reconocimiento de entidades (NER).
try:
    nlp_intent = spacy.load("chatbot_model")
    nlp_ner = spacy.load("es_core_news_md")
except OSError as e:
    print(f"Error cargando los modelos de spaCy: {e}")
    nlp_intent = None
    nlp_ner = None

def chatbot_api(request):
    """
    API principal para el chatbot que procesa los mensajes de los usuarios.

    Utiliza modelos de NLP (spaCy) para detectar la intención y extraer entidades
    del mensaje del usuario. Gestiona flujos de conversación multi-paso (ej. reportar mantenimiento)
    y respuestas directas para consultas de un solo paso.
    """
    if not nlp_intent or not nlp_ner:
        return JsonResponse({'response': 'Error interno: Los modelos de lenguaje no están disponibles.'}, status=500)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            if not user_message:
                return JsonResponse({'response': 'No se recibió ningún mensaje.'})

            # --- Procesamiento de Intención y Entidades ---
            doc_intent = nlp_intent(user_message.lower())
            sorted_cats = sorted(doc_intent.cats.items(), key=lambda item: item[1], reverse=True)
            # Se considera una intención válida si su puntuación es > 0.7
            intent = sorted_cats[0][0] if sorted_cats[0][1] > 0.7 else None

            response_data = {"response": "", "suggestions": []}
            conversation_state = request.session.get('conversation_state')
            context_handled = False

            # --- 1. LÓGICA DE CONVERSACIÓN MULTI-PASO ---
            # Gestiona el flujo de conversación para reportar un problema de mantenimiento.
            if conversation_state == 'AWAITING_MAINTENANCE_ASSET_NAME':
                request.session['maintenance_context'] = {'asset_name': user_message}
                request.session['conversation_state'] = 'AWAITING_MAINTENANCE_DESCRIPTION'
                response_data["response"] = f"Entendido, un problema con '{user_message}'. ¿Cuál es la descripción del problema?"
                context_handled = True

            elif conversation_state == 'AWAITING_MAINTENANCE_DESCRIPTION':
                context = request.session.get('maintenance_context', {})
                if 'asset_name' not in context:
                    response_data["response"] = "Ha ocurrido un error. Empecemos de nuevo."
                    response_data["suggestions"] = ["Reportar un problema"]
                    request.session.pop('conversation_state', None)
                    request.session.pop('maintenance_context', None)
                else:
                    context['description'] = user_message
                    request.session['maintenance_context'] = context
                    request.session['conversation_state'] = 'AWAITING_MAINTENANCE_CONFIRMATION'
                    response_data["response"] = f"Ok, voy a crear una solicitud para '{context['asset_name']}' con la descripción: '{user_message}'. ¿Confirmas?"
                    response_data["suggestions"] = ["Sí, confirmo", "No, cancelar"]
                context_handled = True

            elif conversation_state == 'AWAITING_MAINTENANCE_CONFIRMATION':
                context = request.session.get('maintenance_context', {})
                if intent == 'afirmacion':
                    maintenance_id = create_maintenance_request(context.get('asset_name'), context.get('description'))
                    if maintenance_id:
                        response_data["response"] = f"¡Hecho! Se ha creado la solicitud de mantenimiento #{maintenance_id}."
                    else:
                        response_data["response"] = f"Lo siento, no pude crear la solicitud. No encontré un activo con el nombre o ID '{context.get('asset_name')}'."
                elif intent == 'negacion':
                    response_data["response"] = "Ok, he cancelado el proceso."
                else:
                    response_data["response"] = "No he entendido tu respuesta. Por favor, responde 'Sí' para confirmar o 'No' para cancelar."
                    response_data["suggestions"] = ["Sí", "No"]
                # Limpiar estado de conversación
                request.session.pop('conversation_state', None)
                request.session.pop('maintenance_context', None)
                context_handled = True
            
            else:
                # --- 2. LÓGICA DE CONVERSACIÓN DE UN SOLO PASO ---
                # Extraer entidades (como el estado de un activo) del mensaje.
                doc_ner = nlp_ner(user_message.lower())
                entities = {}
                lemmas_estado = ["mantenimiento", "uso", "disponible"]
                for token in doc_ner:
                    if token.lemma_ in lemmas_estado:
                        entities['status'] = token.text
                        break
                
                request.session.pop('chatbot_context', None)

                if intent == "reportar_problema":
                    request.session.pop('maintenance_context', None)
                    request.session['conversation_state'] = 'AWAITING_MAINTENANCE_ASSET_NAME'
                    response_data["response"] = "Entendido. ¿Para qué activo deseas reportar un problema? (Puedes usar el nombre exacto o su ID)"
                    context_handled = True

                elif intent == "saludo":
                    response_data["response"] = "¡Hola! Soy tu asistente virtual."
                    response_data["suggestions"] = ["Reportar un problema", "Listar activos disponibles"]
                    context_handled = True

                elif intent == "despedida":
                    response_data["response"] = "¡Hasta luego! Que tengas un buen día."
                    context_handled = True

                elif intent == "listar_activos_disponibles":
                    assets = get_available_assets()
                    response_data["response"] = "Claro, los activos disponibles son: <ul>" + "".join([f"<li>{a}</li>" for a in assets]) + "</ul>" if assets else "No hay activos disponibles."
                    response_data["suggestions"] = ["Reportar un problema", "Contar activos en uso"]
                    context_handled = True

                elif intent == "contar_activos_por_estado":
                    status = entities.get('status')
                    if status:
                        count = count_assets_by_status(status)
                        response_data["response"] = f"Hay <b>{count}</b> activos en estado de '{status}'."
                        response_data["suggestions"] = ["¿Y en uso?", "Reportar un problema"]
                        request.session['chatbot_context'] = {'intent': 'contar_activos_por_estado'}
                    else:
                        response_data["response"] = "¿De qué estado te gustaría saber la cantidad de activos?"
                    context_handled = True
                
                elif intent == "get_most_recent_loan":
                    loan = get_most_recent_loan()
                    response_data["response"] = f"El préstamo más reciente fue del activo <b>{loan['asset']}</b> por <b>{loan['user']}</b> el <b>{loan['date']}</b>." if loan else "No hay préstamos registrados."
                    response_data["suggestions"] = ["Listar activos disponibles", "Reportar un problema"]
                    context_handled = True

                elif intent == "listar_capacidades":
                    response_data["response"] = ("¡Claro! Esto es lo que puedo hacer:" \
                                               "<ul>" \
                                               "<li>Listar todos los activos que están disponibles.</li>" \
                                               "<li>Contar cuántos activos hay en un estado específico (disponible, en uso, etc.).</li>" \
                                               "<li>Mostrarte cuál fue el último préstamo registrado.</li>" \
                                               "<li>Ayudarte a crear una solicitud de mantenimiento para un activo.</li>" \
                                               "</ul>")
                    response_data["suggestions"] = ["Listar activos disponibles", "Contar activos en uso", "Reportar un problema"]
                    context_handled = True

                # --- 3. FALLBACK Y CONTEXTO SIMPLE ---
                # Si no se manejó la intención, intentar usar el contexto previo o dar una respuesta por defecto.
                if not context_handled:
                    context = request.session.get('chatbot_context')
                    if context and context.get('intent') == 'contar_activos_por_estado' and entities.get('status'):
                        count = count_assets_by_status(entities.get('status'))
                        response_data["response"] = f"Hay <b>{count}</b> activos en estado de '{entities.get('status')}'."
                        request.session['chatbot_context'] = {'intent': 'contar_activos_por_estado'}
                    else:
                        # Limpiar cualquier estado de conversación residual.
                        request.session.pop('conversation_state', None)
                        request.session.pop('maintenance_context', None)
                        response_data["response"] = "Lo siento, no he entendido tu pregunta."
                        response_data["suggestions"] = ["Reportar un problema", "Listar activos disponibles"]

            return JsonResponse(response_data)

        except Exception as e:
            print(f"Error inesperado en la vista del chatbot: {e}")
            return JsonResponse({'error': 'Ha ocurrido un error interno.'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
@require_POST
def reset_chatbot_session(request):
    """
    Limpia el estado de la conversación del chatbot de la sesión del usuario.
    Útil para reiniciar el flujo de conversación.
    """
    try:
        request.session.pop('conversation_state', None)
        request.session.pop('maintenance_context', None)
        return JsonResponse({'status': 'session_cleared'})
    except Exception as e:
        print(f"Error clearing chatbot session: {e}")
        return JsonResponse({'status': 'error'}, status=500)