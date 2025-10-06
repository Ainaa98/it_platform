from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, UserSerializer,
    UserDetailSerializer, ChangePasswordSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAdminUser


class UserRegistrationView(generics.CreateAPIView):
    """
    Колдонуучу каттоо көрүнүсү
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Колдонуучуну түзгөндөн кийин JWT токенди кайтаруу
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # JWT токендерди түзүү
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Колдонуучу ийгиликтүү катталды'
        }, status=status.HTTP_201_CREATED)


class UserViewSet(ModelViewSet):
    """
    Колдонуучулар үчүн ViewSet
    """
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_staff']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login', 'email']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Ар кандай аракеттер үчүн уруксаттарды ырастоо
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrReadOnly | IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Колдонуучулар тизмесин фильтрлөө
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            # Кадимки колдонуучулар өздөрүнүн маалыматтарын гана көрө алышат
            if self.action == 'list':
                return queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Учурдагы колдонуучунун маалыматтарын алуу
        """
        serializer = UserDetailSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Учурдагы колдонуучунун маалыматтарын жаңыртуу
        """
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Пароль өзгөртүү
        """
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'message': 'Пароль ийгиликтүү өзгөртүлдү'})


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Колдонуучу профили көрүнүсү
    """
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
