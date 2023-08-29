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
        
        intersection = set(top_time).intersection(set(bottom_time))
        bottom_env_unique = np.array([t for t in bottom_time if t not in intersection])
        top_env_unique = np.array([t for t in top_time if t not in intersection])
        top_inter_voltage = np.array(interpolate(bottom_env_unique, top_time, top_env_voltage))
        bottom_inter_voltage = np.array(interpolate(top_env_unique, bottom_time, bottom_env_voltage))

        print(top_inter_voltage)
        print("--------------")
        print(bottom_inter_voltage)

        return JsonResponse(data=[], status=status.HTTP_200_OK, safe=False)
    
def generateSecant(ecg : np.ndarray, position: int = 1) -> [(float, float)]:
    data_length = len(ecg)
    new_time = [ecg[0][0]]
    new_voltage = [ecg[0][1]]

    i = 1
    while i < data_length:
        slope_max = -np.Infinity
        i_optimal = None
        window = ecg[i-1][0] + 0.4
        j = i + 1
        while j  <data_length and ecg[j][0] < window:
            print(ecg[j][1], ecg[i][1], ecg[j][0], ecg[i][0])
            slope = ((ecg[j][1] - ecg[i][1]) / (ecg[j][0] - ecg[i][0])) * position
            if slope >= slope_max:
                slope_max = slope
                i_optimal = j
            j += 1
        if i_optimal != None:
            new_time.append(ecg[i_optimal][0])
            new_voltage.append(ecg[i_optimal][1])
            i = i_optimal
        else:
            i = j

        return (np.interp, np.array(new_time), np.array(new_voltage))
    
#         while i < dataLength {
#             var slopeMax : Double = -Double.infinity
#             var iOptimal : Int? = nil
            
#             let window = voltageReadings[i - 1].1 + 0.4
#             var j : Int = i + 1
#             while j < dataLength && voltageReadings[j].1 < window {
#                 let slope = ((voltageReadings[j].2 - voltageReadings[i].2) / (voltageReadings[j].1 - voltageReadings[j].1)) * position
                
#                 if slope >= slopeMax {
#                     slopeMax = slope
#                     iOptimal = j
#                 }
#                 j += 1
#             }
#             if let optimal = iOptimal {
#                 newTime.append(voltageReadings[optimal].1)
#                 newVoltage.append(voltageReadings[optimal].2)
# //                newReadings.append((type, voltageReadings[optimal].1, voltageReadings[optimal].2))
#                 i = optimal
#             } else {
#                 i = j
#             }
#         }
        
#         // To make sure that both top and bottom secant remains the same size to be subtracted from.
#         let controlVector : [ Double ] = vDSP.ramp(in: 0 ... Double(newTime.count) - 1, count: 2048)
#         print(newTime.count)
#         print(newVoltage.count)
# //        let resultTime : [Double] = vDSP.linearInterpolate(elementsOf: newTime, using: controlVector)
# //        let resultVoltage : [Double] = vDSP.linearInterpolate(elementsOf: newVoltage, using: controlVector)

#         return []
#     }