from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
import json
from .services import *

# Create request handler method for forms requests
@csrf_exempt
def handle_forms_request(request):
    print(str(request.method))
    if request.method == 'GET':
        response = get_form(request)
    elif request.method == 'POST':
        response = post_form(json.loads(request.body))
    elif request.method == 'DELETE':
        response = delete_form(request)
    return JsonResponse(response, safe=False)

# Create request handler method for questions requests
@csrf_exempt
def handle_questions_request(request):
    print(str(request.method))
    if request.method == 'GET':
        response = get_question(request)
    elif request.method == 'POST':
        response = post_question(json.loads(request.body))
    elif request.method == 'DELETE':
        response = delete_question(request)
    elif request.method == 'PUT':
        response = put_question(json.loads(request.body))
    return JsonResponse(response, safe=False)

# Controller methods
# Process GET requests for forms 
def get_form(request):
    pass

# Process CREATE requests for forms 
def post_form(request):
    pass

# Process DELETE requests for forms
def delete_form(request):
    pass

# Process CREATE requests for questions 
def post_question(request):
    pass

# Process DELETE requests for questions 
def delete_question(request):
    pass

# Process PUT requests for questions 
def put_question(request):
    pass