from rest_framework import serializers

from apps.statistic_app.models import StatisticsModel


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticsModel
        fields = ('id', 'name', 'value', 'created_at')
