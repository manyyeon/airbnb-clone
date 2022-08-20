from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room  # Room 모델 사용
        fields = "__all__"  # 모든 필드 포함
