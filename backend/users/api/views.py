from rest_framework import generics
from users.api.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт регистрации нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
