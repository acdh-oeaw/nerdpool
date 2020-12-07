from rest_framework import serializers

from . models import NerSample, NerDataSet


class NerSampleSerializer(serializers.ModelSerializer):

    spans = serializers.ListField(source="get_spans")

    class Meta:
        model = NerSample
        fields = [
            'id',
            'text',
            'spans',
        ]
