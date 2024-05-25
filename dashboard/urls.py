from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'utility-status', UtilityStatusViewSet)
router.register(r'grid-status', GridStatusViewSet)
router.register(r'security-alerts', SecurityAlertViewSet)
router.register(r'honeypots', HoneypotViewSet)
router.register(r'weekly-data', WeeklyDataViewSet)
router.register(r'component-status', ComponentStatusViewSet)
router.register(r'dashboard-data', DashboardDataViewSet)
router.register(r'generation-data', GenerationDataViewSet)
router.register(r'consumption-data', ConsumptionDataViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
