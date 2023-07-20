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
    if request.method == 'GET':
        hb_data = Biometrics.objects.all()
        serializer = BiometricSerializer(hb_data, many=True)
        return JsonResponse(serializer.data[-1])
    elif request.method == 'PUT':
        serializer = BiometricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        serializer = BiometricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    