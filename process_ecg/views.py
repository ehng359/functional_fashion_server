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

        # Process into JSON format, split it into three columns, look at research algorithm
        request.data["ecgData"]
        print("test")
        return JsonResponse(data=[], status=status.HTTP_200_OK)
        
        # id!
        # ecgData: '[{"voltage":0.08044256591796875,"type":"Raw","time":29.978515625},
        # {"voltage":0.080256767272949225,"type":"Raw","time":29.98046875},
        # {"voltage":0.079877677917480461,"type":"Raw","time":29.982421875},
        # {"voltage":0.079301620483398436,"type":"Raw","time":29.984375},
        # {"voltage":0.078527038574218749,"type":"Raw","time":29.986328125},
        # {"voltage":0.077554138183593746,"type":"Raw","time":29.98828125},
        # {"voltage":0.076383575439453122,"type":"Raw","time":29.990234375},
        # {"voltage":0.075017181396484375,"type":"Raw","time":29.9921875},
        # {"voltage":0.073457443237304687,"type":"Raw","time":29.994140625},
        # {"voltage":0.071707244873046874,"type":"Raw","time":29.99609375},
        # {"voltage":0.06977275085449218,"type":"Raw","time":29.998046875}]'}
    

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