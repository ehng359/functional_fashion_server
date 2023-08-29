# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status

import numpy as np

# Create your views here.
@api_view(['POST', 'GET'])
def process_ecg_data (request):
    # Retrieves all of the values from every recorded instance provided (all sources)
    if request.method == 'GET':
        print("GET")
        return Response([], status=200)

    # Appends to the existing list of instances
    elif request.method == 'POST':
        print(request.data)
        print("test")
    

def generateSecant(voltageReadings : [(float, float)], position: int) -> [(float, float)]:
    dataLength = len(voltageReadings)
    type = "Top" if position == 1 else "Bottom"
    # newTime = [voltageReadings[0][0]]
#         var newTime : [Double] = [voltageReadings.first!.1]
#         var newVoltage : [Double] = [voltageReadings.first!.2]
# //        var newReadings : [(String, Double, Double)] = [(type, voltageReadings.first!.1, voltageReadings.first!.2)]
#         var i : Int = 1
        
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