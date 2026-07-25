import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .engine import get_predictor


def index(request):
    return render(request, 'predictor/index.html')


@csrf_exempt
def predict(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        p = get_predictor()
        predicted_age, years_left = p.predict(data)
        factors = p.factor_impacts(data)
        health  = p.health_score(data)
        return JsonResponse({
            'predicted_age': predicted_age,
            'years_left':    years_left,
            'current_age':   float(data['age']),
            'factors':       factors,
            'health_score':  health,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
