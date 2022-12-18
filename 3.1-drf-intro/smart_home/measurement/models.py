from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    desctiption = models.CharField(max_length=100)


class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
