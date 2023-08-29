# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status

import numpy as np, json, ast

# Create your views here.
@api_view(['POST', 'GET'])
def process_ecg_data (request):
    # Retrieves all of the values from every recorded instance provided (all sources)
    if request.method == 'GET':
        print("GET")
        return Response([], status=200)

    # Appends to the existing list of instances
    elif request.method == 'POST':
        # Setting up the envelopes encasing the ECG data.
        ecgData = ast.literal_eval(request.data["ecgData"])
        times = np.vstack([ float(ecg["time"]) for ecg in ecgData ])
        voltages = np.vstack([ float(ecg["voltage"]) for ecg in ecgData ])
        tv_input = np.hstack((times, voltages))

        interpolate, top_time, top_env_voltage = generateSecant(tv_input)
        _, bottom_time, bottom_env_voltage = generateSecant(tv_input, position=-1)
        # print("Length of top times: ", len(top_time))
        # print("Length of bottom times: ", len(bottom_time))
        intersection = set(top_time).intersection(set(bottom_time))
        print(intersection, len(intersection))
        bottom_env_unique = np.array([t for t in bottom_time if t not in intersection])
        top_env_unique = np.array([t for t in top_time if t not in intersection])
        top_inter_voltage = np.array(interpolate(bottom_env_unique, top_time, top_env_voltage))
        bottom_inter_voltage = np.array(interpolate(top_env_unique, bottom_time, bottom_env_voltage))

        # print(top_inter_voltage)
        # print("--------------")
        # print(bottom_inter_voltage)
        # print("length of unique times", top_env_unique, len(top_env_unique), bottom_env_unique, len(bottom_env_unique)) 

        return JsonResponse(data=[], status=status.HTTP_200_OK, safe=False)
    
def generateSecant(ecg : np.ndarray, position: int = 1) -> [(float, float)]:
    data_length = len(ecg)
    times = ecg[:,0]
    voltages = ecg[:,1]

    new_time = [times[0]]
    new_voltage = [voltages[1]]

    i = 1
    while i < data_length:
        slope_max = -np.Infinity
        i_optimal = None
        window = times[i-1] + 0.4
        j = i + 1
        while j < data_length and ecg[j][0] < window:
            slope = ((voltages[j] - voltages[i]) / (times[j] - times[i])) * position if times[j] != times[i] else -np.Infinity
            if slope >= slope_max:
                slope_max = slope
                i_optimal = j
            j += 1
        if i_optimal != None:
            new_time.append(times[i_optimal])
            new_voltage.append(voltages[i_optimal])
            i = i_optimal
        else:
            i = j
    return (np.interp, np.array(new_time), np.array(new_voltage))