# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
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
        hb_data = Biometrics.objects.all().delete()
        serializer = BiometricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Appends to the existing list of instances
    elif request.method == 'POST':
        serializer = BiometricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    