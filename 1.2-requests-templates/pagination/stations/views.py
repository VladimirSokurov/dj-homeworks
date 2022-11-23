from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV
import csv


def open_phonebook(name):
    bus_station = []
    with open('data-398-2018-08-30.csv', newline='\n', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bus_station.append({
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District'],
            })
    return bus_station


bus_station = open_phonebook(BUS_STATION_CSV)


# CONTENT = [i for i in bus_station]
# print(CONTENT)


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(bus_station, 10)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)

# def pagi(request):
#     page_number = int(request.GET.get("page", 1))
#     paginator = Paginator(CONTENT, 10)
#     page = paginator.get_page(page_number)
#     context = {
#         'page': page
#     }
#     return render(request, 'pagi.html', context)
