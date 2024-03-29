from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="가까? 마까?",
        default_version='v1',
        description="가까? 마까? 프로젝트 API",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="wogur981208@gmail.com"),
        license=openapi.License(name="Gaggamagga License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('reviews/',include('reviews.urls')),
    path('places/',include('places.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-json'), 
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('chat/', include('chat.urls')),
    path('notification/', include('notification.urls')),
    path('search/', include('search.urls')),
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)