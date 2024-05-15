from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from core.permissions import IsAuthorEntry
from core.serializers import UserSerializer, UserDetailSerializer
from .models import RentU


class UserCreateView(generics.CreateAPIView):
    """Добавление нового пользователя"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = RentU.objects.create_user(username, email)
        user.set_password(password)
        user.save()
        return Response("User created")


class UserListAPIviews(generics.ListAPIView):
    queryset = RentU.objects.exclude(is_staff=True).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailAPIviews(generics.UpdateAPIView):
    queryset = RentU.objects.exclude(is_staff=True).order_by('-date_joined')
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthorEntry]

    def get(self, request, pk):
        items_list = RentU.objects.get(id=pk)
        serializer = UserDetailSerializer(items_list)
        return Response(serializer.data)
