from django.urls import path
from measurement.views import *

urlpatterns = [
    path('sensor/', SensorView.as_view()),
    path('sensor/<pk>/', SensorDetailView.as_view()),
    path('measurement/', MeasurementView.as_view()),
]
