from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import RentU, Orders


class FilterOrdersistSerializer(serializers.ListSerializer):
    """Фильтр аренд, только активные"""

    def to_representation(self, data):
        data = data.filter(active=True)
        return super().to_representation(data)

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentU
        fields = ['id', 'username', 'lang', 'password']


class OrdersSerializer(serializers.ModelSerializer):
    renter = serializers.SlugRelatedField(slug_field="username", read_only=True)
    rented_car = serializers.SlugRelatedField(slug_field="name_car_en", read_only=True)

    class Meta:
        list_serializer_class = FilterOrdersistSerializer
        model = Orders
        fields = ['renter', 'rented_car', 'date_begin', 'date_end', 'active']

class UserSerializer(serializers.ModelSerializer):
    order = OrdersSerializer(many=True)
    class Meta:
        model = RentU
        fields = ['id', 'username', 'email', 'lang', 'password', 'first_name', 'last_name', 'order']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentU
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'lang')


