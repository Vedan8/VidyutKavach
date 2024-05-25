from rest_framework import viewsets
from .models import *
from .serializers import *
from .models import GenerationData, ConsumptionData

class UtilityStatusViewSet(viewsets.ModelViewSet):
    queryset = UtilityStatus.objects.all()
    serializer_class = UtilityStatusSerializer

class GridStatusViewSet(viewsets.ModelViewSet):
    queryset = GridStatus.objects.all()
    serializer_class = GridStatusSerializer

class SecurityAlertViewSet(viewsets.ModelViewSet):
    queryset = SecurityAlert.objects.all()
    serializer_class = SecurityAlertSerializer

class HoneypotViewSet(viewsets.ModelViewSet):
    queryset = Honeypot.objects.all()
    serializer_class = HoneypotSerializer

class WeeklyDataViewSet(viewsets.ModelViewSet):
    queryset = WeeklyData.objects.all()
    serializer_class = WeeklyDataSerializer

class ComponentStatusViewSet(viewsets.ModelViewSet):
    queryset = ComponentStatus.objects.all()
    serializer_class = ComponentStatusSerializer

class IdsViewSet(viewsets.ModelViewSet):
    queryset = Ids.objects.all()
    serializer_class = IdsSerializer

class FirewallViewSet(viewsets.ModelViewSet):
    queryset = FireWall.objects.all()
    serializer_class = FirewallSerializer

class Co2ViewSet(viewsets.ModelViewSet):
    queryset = CO2Emmision.objects.all()
    serializer_class = Co2Serializer

class EnergyEfficiencyViewSet(viewsets.ModelViewSet):
    queryset = EnergyEfficiency.objects.all()
    serializer_class = EnersyEfficiencySerializer

class DashboardDataViewSet(viewsets.ModelViewSet):
    queryset = DashboardData.objects.all()
    serializer_class = DashboardDataSerializer

class GenerationDataViewSet(viewsets.ModelViewSet):
    queryset = GenerationData.objects.all()
    serializer_class = GenerationDataSerializer

class ConsumptionDataViewSet(viewsets.ModelViewSet):
    queryset = ConsumptionData.objects.all()
    serializer_class = ConsumptionDataSerializer