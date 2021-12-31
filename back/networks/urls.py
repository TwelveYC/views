from django.urls import path
from .views import scaleFreeNetworks, smallWorldNetworks, randomNetworks, evolution_networks, osmnx_map

urlpatterns = [
    path("sf/", scaleFreeNetworks, name="scaleFreeNetworks"),
    path("sw/", smallWorldNetworks, name="smallWorldNetworks"),
    path("random/", randomNetworks, name="randomNetworks"),
    path("evolution/", evolution_networks, name="evolution"),
    path("map/", osmnx_map, name="map"),
]