from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger документация үчүн конфигурация
schema_view = get_schema_view(
    openapi.Info(
        title="IT Platform API",
        default_version='v1',
        description="""
        IT багыты боюнча окутуу платформасынын API документациясы.

        Бул API Django REST Framework жана JWT аутентификациясы менен иштейт.

        ## Эскертүүлөр:
        - Бардык API endpointтери JWT токен менен корголгон (каттоодон башка)
        - Каттоо үчүн `/api/users/register/` endpointин колдонуңуз
        - Аутентификация үчүн `/api/token/` endpointин колдонуңуз
        - Swagger UIда "Authorize" баскычын басып, токенди киргизиңиз: "Bearer your_access_token"
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@it-platform.kg"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # API URLs
    path('api/', include('users.urls')),
    path('api/', include('courses.urls')),

    # API Documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

# Debug режимда статикалык жана медиа файлдар үчүн
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "IT Platform Administration"
admin.site.site_title = "IT Platform Admin"
admin.site.index_title = "Welcome to IT Platform Admin Panel"