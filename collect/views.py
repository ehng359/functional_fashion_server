# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import subprocess, json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Biometrics
from .serializers import BiometricSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['POST', 'GET', 'PUT'])
def get_hb_data (request):
    # Retrieves all of the values from the recorded instance
    if request.method == 'GET':
        hb_data = Biometrics.objects.all()
        serializer = BiometricSerializer(hb_data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # Updates the list of instances with a new value
    elif request.method == 'PUT':
        process = subprocess.Popen(['./makeData.sh'], stdout=subprocess.PIPE)
        message = process.communicate()[0].decode()

        file_name = message.split("\n")[-2]
        file = open(file_name, "r")
        json_data = json.load(file)

        if process.returncode == 0:
            hb_data = Biometrics.objects.all().delete()
            return Response({"local_save": "successful", "type" : "JSON", "JSON_Content" : json_data}, status=200)
        
        return Response({"local_save": "undefined", "type" : "JSON", "file_name" : message}, status=400)
    
    # Appends to the existing list of instances
    elif request.method == 'POST':
        serializer = BiometricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    