from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.roomDetail),
    path("search/", views.search, name="search"),
    path("", views.roomList),
]
