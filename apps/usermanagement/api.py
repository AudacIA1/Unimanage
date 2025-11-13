from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import DashboardPreference

@require_http_methods(["GET","POST"])
def dashboard_preferences(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'unauthenticated'}, status=401)
    if request.method == 'GET':
        pref, _ = DashboardPreference.objects.get_or_create(user=request.user)
        return JsonResponse(pref.prefs or {}, status=200)
    else:
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return JsonResponse({'error': 'invalid json'}, status=400)
        pref, _ = DashboardPreference.objects.get_or_create(user=request.user)
        pref.prefs = payload
        pref.save()
        return JsonResponse({'ok': True}, status=200)
