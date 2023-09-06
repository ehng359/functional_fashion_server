# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.core import serializers
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework import status

import numpy as np, neurokit2 as nk, json, ast, subprocess, os
from scipy.signal import find_peaks, butter, sosfiltfilt

SCI_PY_METHOD = 0
DB_DIFF_METHOD = 1

@api_view(['POST', 'GET'])
def process_ecg_data (request):
    if request.method == 'GET':
        return Response([], status=200)

    # Appends to the existing list of instances
    elif request.method == 'POST':
        # Setting up the envelopes encasing the ECG data.
        ecgData = ast.literal_eval(request.data["ecgData"])
        times = [ float(ecg["time"]) for ecg in ecgData ]
        voltages = [ float(ecg["voltage"]) for ecg in ecgData ]

        if "TEST" in request.data:
            if os.path.isfile("./data/test_ecg_time.json") and os.path.isfile("./data/test_ecg_voltage.json"):
                file_time = open("./data/test_ecg_time.json", "r")
                times = ast.literal_eval(file_time.read())
                file_time.close()

                file_voltage = open("./data/test_ecg_voltage.json", "r")
                voltages = ast.literal_eval(file_voltage.read())
                file_voltage.close()

            with open("./data/test_ecg_time.json", "w") as file_time:
                file_time.write(json.dumps(times))
                file_time.close()

            with open("./data/test_ecg_voltage.json", "w") as file_volt:
                file_volt.write(json.dumps(voltages))
                file_volt.close()

            # subprocess.Popen(['python3', 'emailUserData.py', '-n', "test_ecg_time.json", '-e', "3dward.ng@gmail.com"], stdout=subprocess.PIPE)
            # subprocess.Popen(['python3', 'emailUserData.py', '-n', "test_ecg_voltage.json", '-e', "3dward.ng@gmail.com"], stdout=subprocess.PIPE)
        filtered_voltages = band_pass_filter(data=voltages, lower_freq=10, upper_freq=100, sampling_rate=1000, poles=5)

        est_t = np.linspace(0, 30, 30000)
        est_v = np.array(np.interp(est_t, times, filtered_voltages))
        tv_input = np.hstack((np.vstack(est_t), np.vstack(est_v)))
        peak_time, _ = find_r_peaks(tv_input)
        
        hrv = compute_HRV(peak_time)
        est_rr = nk.ecg_rsp(est_v, sampling_rate=1000)
        rr_peaks, _ = find_peaks(est_rr)
        
        return JsonResponse(data={ "hrv" : hrv, "rr" : len(rr_peaks) * 2 }, status=status.HTTP_200_OK, safe=False)
    
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

def find_r_peaks (env : np.ndarray, method : int = SCI_PY_METHOD) -> None:
    if method == SCI_PY_METHOD:
    # --------------    Method 1    ----------------
        '''
            scipy.find_peaks method which specializes in searching for jumps in data (enabling R-Peaks to be)
            easily identifiable.
        '''
        indices, _ = find_peaks(env[:,1], distance=150, prominence=1)
        time_vals = sorted([env[:,0][index] for index in indices])
        volt_vals = np.interp(time_vals, env[:,0], env[:,1])
        return time_vals, volt_vals

    elif method == DB_DIFF_METHOD:
    # ------------      Method 2        -------------
        '''
            Double difference method proposed in: 
            https://www.sciencedirect.com/science/article/pii/S2212017312004227
            (UNFINISHED)
        '''
        voltages = env[:,1]
        dif1 = []
        for i in range(0, len(voltages)-1):
            dif1.append(voltages[i+1] - voltages[i])

        dif2 = []
        for j in range(0, len(dif1) -1):
            dif2.append(dif1[j+1] - dif1[j])
        
        db_diff = np.array(dif2) ** 2
        times = np.delete(times, [len(times) - 1, len(times) - 2])
        
        peak_differences = np.hstack((np.vstack(times), np.vstack(db_diff)))
        peak_differences = peak_differences[peak_differences[:,1].argsort()[::-1]]

        max = peak_differences[0][1]
        threshold = max * 0.03
        selected = []

        # Optimize via combining different ranges together.
        coverage = list()
        for i in range(1, len(peak_differences)):
            if peak_differences[i][1] < threshold:
                break

            range_exists = False
            for ranges in coverage:
                if ranges[0] <= peak_differences[i][0] and peak_differences[i][0] <= ranges[1]:
                    range_exists = True
                    break
            if not range_exists:
                selected.append(peak_differences[i])
                coverage.append((peak_differences[i][0] - 0.075, peak_differences[i][0] + 0.075))
        
        return selected
    return

def compute_HRV(r_peak_times) :
    rr_intervals = []
    prev = r_peak_times[0]
    for i in range(1, len(r_peak_times)):
        rr_intervals.append(r_peak_times[i] - prev)
        prev = r_peak_times[i]

    rr_intervals = np.array(rr_intervals) * 1000
    prev = rr_intervals[0]
    sum_of_squared_diff = 0
    for i in range(1, len(rr_intervals)):
        rr_diff = rr_intervals[i] - prev
        sum_of_squared_diff += rr_diff ** 2
    RMSSD = np.sqrt(sum_of_squared_diff / (len(rr_intervals) - 1))
    return RMSSD

def low_pass_filter(data : np.ndarray, cutoff : float, sample_rate : float, poles : int):
    sos = butter(poles, cutoff, 'lowpass', fs=sample_rate, output="sos")
    filtered_data = sosfiltfilt(sos, data)
    return filtered_data

def band_pass_filter(data : np.ndarray, lower_freq : float, upper_freq: float, sample_rate : float, poles : int):
    sos = butter(poles, [lower_freq, upper_freq], 'bandpass', fs=sample_rate, output="sos")
    filtered_data = sosfiltfilt(sos, data)
    return filtered_data