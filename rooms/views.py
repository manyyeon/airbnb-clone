from rest_framework import status
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django_countries import countries
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RoomSerializer
from . import models


@api_view(["GET"])
def roomList(request):
    rooms = models.Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def roomDetail(request, pk):
    room = get_object_or_404(models.Room, pk=pk)

    if request.method == "GET":
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    elif request.method == "DELETE":
        room.delete()
        data = {"pk": pk}
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = RoomSerializer(instance=room, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room


def search(request):
    print(request.GET)
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("price", 0))
    bedrooms = int(request.GET.get("price", 0))
    beds = int(request.GET.get("price", 0))
    baths = int(request.GET.get("price", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(request, "rooms/search.html", {**form, **choices})
