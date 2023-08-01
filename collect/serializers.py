from rest_framework import serializers
from .models import Biometrics
class BiometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometrics
        fields = ['date', 'heartBeat', 'respiratoryRate', 'heartBeatVar', 'restingHeartRate']