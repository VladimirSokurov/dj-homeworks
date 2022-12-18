from django.forms import model_to_dict
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response

from .serializers import *
from .models import *


class SensorView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        new_sensor = Sensor.objects.create(
            name=request.data['name'],
            desctiption=request.data['desctiption']
        )
        return Response({'new_sensor': model_to_dict(new_sensor)})


class SensorDetailView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def patch(self, request, pk):
        changed_sensor = Sensor.objects.get(pk=pk)
        serializer = SensorSerializer(changed_sensor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'changed_sensor': model_to_dict(changed_sensor)})
        return Response(code=400, data="wrong parameters")


class MeasurementView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer2
