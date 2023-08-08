from rest_framework import serializers
from .models import Biometrics, Users
class BiometricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biometrics
        fields = ['watchUser', 'date', 'heartBeat', 'respiratoryRate', 'heartBeatVar', 'restingHeartRate', 'valence', 'arousal']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'biometricData']