from rest_framework import serializers

from . models import NerSample, NerDataSet


class NerSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NerSample
        fields = [
            'id',
            'text',
        ]
