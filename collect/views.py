# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import subprocess, json, datetime, re 
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
        # ? starts the query
        # & separates each parameter
        # = assigns right-hand value to left-hand value
        '''
        required:
            watchID
        filters:
            since_date -> "yyyy-mm-dd"
            since_time -> "hh:mm:ss"
            past -> "x [weeks/days/hours/minutes]" (old/live data)
            num_instances -> "x" (old/live data)
            session_id -> "file_name" - yet to implement
        '''
        params = dict(request.GET)
        if len(params) == 0:
            hb_data = Biometrics.objects.all()
            serializer = BiometricSerializer(hb_data, many=True)
            return JsonResponse(serializer.data, safe=False)
        
        # There are provided parameters in the GET request which provide filters we may search for.
        watch_identifier = params["id"] if "id" in params else None
        if len(watch_identifier) != 1:
            return Response("No WatchID provided.", status=400)
        desired_time = None
        dateFilterEnabled = False

        
        since_date = params["since_date"] if "since_date" in params and "past" not in params else None
        since_time = params["since_time"] if "since_time" in params and "past" not in params else None
        if since_time or since_date:
            dateFilterEnabled = True
            current_time = datetime.datetime.today()
            year, month, day, hours, minutes, seconds = current_time.year, current_time.month, current_time.day, 0, 0, 0
            if since_date:
                since_date = since_date[0].split("-")
                (year, month, day) = (int(since_date[0]), int(since_date[1]), int(since_date[2]))
            if since_time:
                since_time = since_time[0].split(":")
                (hours, minutes, seconds) = (int(since_time[0]), int(since_time[1]), int(since_time[2]))
            desired_time = datetime.datetime(year, month, day, hours, minutes, seconds)
        
        # Date will be passed in by { "past": "(numeric) (metric)" } 
        past = params["past"] if "past" in params and "since" not in params else None
        if past:
            dateFilterEnabled = True
            current_time = datetime.datetime.now()
            past = past[0].split("_")
            past_value = float(past[0])
            past_metric = past[1]
            match(past_metric):
                case "seconds" | "second":
                    desired_time = current_time - datetime.timedelta(seconds=past_value)
                case "minutes" | "minute":
                    desired_time = current_time - datetime.timedelta(minutes=past_value)
                case "hours" | "hour":
                    desired_time = current_time - datetime.timedelta(hours=past_value)
                case "days" | "day":
                    desired_time = current_time - datetime.timedelta(days=past_value)
                case _:
                    print("defaulted")
        
        num_instances = int(params["num_instances"][0]) if "num_instances" in params else None

        user = Users.objects.get(id=watch_identifier[0])
        data = user.biometricData.all()
        ret = []
        if dateFilterEnabled:
            for datum in reversed(data):
                if num_instances == 0:
                    break

                # Parsing biometric values to evaluate if in range
                datum_date = re.split('-| |:', datum.date)
                datum_date = [int(value) if value else None for value in datum_date]
                datum_date.pop()
                datum_date_object = datetime.datetime(*datum_date)
                
                if datum_date_object > desired_time:
                    ret.append(datum)
                if num_instances:
                    num_instances -= 1
        elif num_instances:
            for datum in reversed(data):
                if num_instances == 0:
                    break
                ret.append(datum)
                if num_instances:
                    num_instances -= 1
        serialized_biometrics = serializers.serialize(format="json", queryset=list(reversed(ret)))
        data = json.loads(serialized_biometrics)
        data_raw = [biometric['fields'] for biometric in data]
        return JsonResponse(data_raw, safe=False)

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
    