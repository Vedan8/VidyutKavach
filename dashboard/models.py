from django.db import models

class UtilityStatus(models.Model):
    data = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    ]

    def __str__(self):
        return self.data

class GridData(models.Model):
    _id = [
        ('input', 'Input'),
        ('output', 'Output'),
        ('storage', 'Storage'),
    ]
    total_value = models.FloatField()

class GridStatus(models.Model):
    data=models.ManyToManyField(GridData)
    def __str__(self):
        return self.data
    
class SecurityAlert(models.Model):
    ip = models.GenericIPAddressField()
    is_read=models.BooleanField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source_ip
    
class Honeypot(models.Model):
    total = models.IntegerField()
    active = models.IntegerField()
    detections = models.IntegerField()

    def __str__(self):
        return f"Active: {self.active}/{self.total}, Detections: {self.detections}"
    
class FireWall(models.Model):
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    ]

class Ids(models.Model):
    STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
    ]
    
class ComponentStatus(models.Model):
    typeName = models.CharField(max_length=50)
    activeCount = models.IntegerField()

    def __str__(self):
        return f"{self.typeName} - {self.activeCount}"
    
class EnergyEfficiency(models.Model):
    value = models.FloatField()
    unit = models.CharField(max_length=10, default='%')
    def __str__(self):
        return f"Efficiency: {self.energy_efficiency_value}{self.energy_efficiency_unit}"
    
class CO2Emmision(models.Model):
    value = models.FloatField()
    unit = models.CharField(max_length=10, default='tons')

    def __str__(self):
        return f"CO2: {self.co2_value}{self.co2_unit}"


class Metric(models.Model):
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.value} at {self.date}"
    
class GenerationData(models.Model):
    solar_plants = models.ManyToManyField(Metric, related_name='solar_metrics')
    wind_turbines_plants = models.ManyToManyField(Metric, related_name='wind_metrics')
    utility = models.ManyToManyField(Metric, related_name='utility_metrics')

    def __str__(self):
        return "Generation Data"
    
class ConsumptionData(models.Model):
    residential = models.ManyToManyField(Metric, related_name='residential_metrics')
    commercial = models.ManyToManyField(Metric, related_name='commercial_metrics')
    industrial = models.ManyToManyField(Metric, related_name='industrial_metrics')

    def __str__(self):
        return "Consumption Data"

class WeeklyData(models.Model):
    name = models.CharField(max_length=50)
    data=models.ManyToManyField(Metric)
    totalWeeklyValue=models.IntegerField()

    def __str__(self):
        return self.name

class DashboardData(models.Model):
    utility_status = models.OneToOneField(UtilityStatus, on_delete=models.CASCADE)
    grid_status = models.ManyToManyField(GridStatus)
    weekly_data = models.ManyToManyField(WeeklyData)
    active_components = models.ManyToManyField(ComponentStatus)
    ids=models.OneToOneField(Ids,on_delete=models.CASCADE)
    firewall=models.OneToOneField(FireWall,on_delete=models.CASCADE)
    honeypot = models.OneToOneField(Honeypot, on_delete=models.CASCADE)
    co2_emission=models.OneToOneField(CO2Emmision, on_delete=models.CASCADE)
    energy_efficiency = models.OneToOneField(EnergyEfficiency, on_delete=models.CASCADE)
    security_alerts = models.ManyToManyField(SecurityAlert)

    def __str__(self):
        return f"Dashboard Data as of {self.utility_status.last_updated}"