from django.contrib import admin
from django.urls import path
from calculator.views import get_recipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'<str:name>/', get_recipe)
]
