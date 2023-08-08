# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import subprocess, json
from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view
from .models import Biometrics, Users
from .serializers import BiometricSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['POST', 'GET', 'PUT'])
def get_hb_data (request):
    # Retrieves all of the values from every recorded instance provided (all sources)
    if request.method == 'GET':
        hb_data = Biometrics.objects.all()
        serializer = BiometricSerializer(hb_data, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    # Updates the list of instances with a new value
    elif request.method == 'PUT':
        user = Users.objects.get(id=request.data["id"])
    
        serialized_biometrics = serializers.serialize(format="json", queryset=user.biometricData.all())
        user.biometricData.all().delete()

        data = json.loads(serialized_biometrics)
        data_raw = [biometric['fields'] for biometric in data]
        data = json.dumps(data_raw, indent=4)

        # Simply creates the directories to store the information.
        process = subprocess.Popen(['./makeData.sh'], stdout=subprocess.PIPE)
        message = process.communicate()[0].decode()

        file_name = message.split("\n")[-2]
        file = open(file_name, "w")
        file.write(data)

        if process.returncode == 0:
            return Response({"local_save": "successful", "type" : "JSON", "JSON_Content" : data_raw}, status=200)
        return Response({"local_save": "undefined", "type" : "JSON", "JSON_Content" : None}, status=400)

    # Appends to the existing list of instances
    elif request.method == 'POST':
        user = Users.objects.get_or_create(id=request.data["id"])[0]
        biometric_data = request.data
        biometric_data["watchUser"] = user
        biometric_data.pop("id")

        serializer = BiometricSerializer(data=biometric_data)
        if serializer.is_valid():
            serializer.save() 
            user.biometricData.add(Biometrics.objects.last())
            user.save()
            return Response(serializer.data, status=200)
        return Response({}, status=400)
    