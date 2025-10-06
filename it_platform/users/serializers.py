from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Колдонуучу каттоо сериализатору пароль тастыктоо менен
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'},
        label="Пароль"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Парольду тастыктоо"
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'password', 'password2', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def validate(self, attrs):
        """
        Парольдор дал келерин текшерүү
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Парольдор дал келбейт."})
        return attrs

    def create(self, validated_data):
        """
        Жаңы колдонуучуну түзүү
        """
        validated_data.pop('password2')  # password2 өчүрүү
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Колдонуучу маалыматтары үчүн сериализатор
    """

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_active', 'is_staff', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserDetailSerializer(UserSerializer):
    """
    Толук колдонуучу маалыматтары үчүн сериализатор
    """

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['is_superuser']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Пароль өзгөртүү сериализатору
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Жаңы парольдор дал келбейт."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Эски пароль туура эмес.")
        return value