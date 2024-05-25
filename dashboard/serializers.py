from rest_framework import serializers
from .models import *

class UtilityStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityStatus
        fields = '__all__'

class GridStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridStatus
        fields = '__all__'

class SecurityAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityAlert
        fields = '__all__'

class HoneypotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Honeypot
        fields = '__all__'

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'

class WeeklyDataSerializer(serializers.ModelSerializer):
    metrics = MetricSerializer(many=True)

    class Meta:
        model = WeeklyData
        fields = '__all__'

class ComponentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentStatus
        fields = '__all__'

class IdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ids
        fields = '__all__'

class FirewallSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireWall
        fields = '__all__'

class Co2Serializer(serializers.ModelSerializer):
    class Meta:
        model = CO2Emmision
        fields = '__all__'

class EnersyEfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyEfficiency
        fields = '__all__'

class DashboardDataSerializer(serializers.ModelSerializer):
    utility_status = UtilityStatusSerializer()
    grid_status = GridStatusSerializer(many=True)
    security_alerts = SecurityAlertSerializer(many=True)
    honeypot = HoneypotSerializer()
    weekly_data = WeeklyDataSerializer(many=True)
    active_components = ComponentStatusSerializer(many=True)
    firewall=FirewallSerializer()
    ids=IdsSerializer()
    co2_emission=Co2Serializer()
    energy_efficiency=EnersyEfficiencySerializer()

    class Meta:
        model = DashboardData
        fields = '__all__'

class GenerationDataSerializer(serializers.ModelSerializer):
    solar_plants = MetricSerializer(many=True)
    wind_turbines_plants = MetricSerializer(many=True)
    utility = MetricSerializer(many=True)

    class Meta:
        model = GenerationData
        fields = '__all__'

class ConsumptionDataSerializer(serializers.ModelSerializer):
    residential = MetricSerializer(many=True)
    commercial = MetricSerializer(many=True)
    industrial = MetricSerializer(many=True)

    class Meta:
        model = ConsumptionData
        fields = '__all__'
