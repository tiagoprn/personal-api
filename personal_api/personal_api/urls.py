from django.contrib import admin
from django.urls import path, re_path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views

from core import views as core_views
from personal_api import views as project_views

schema_view = get_schema_view(
    openapi.Info(title='Swagger API', default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    path(
        '', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'
    ),
    path(
        'api/token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'health-check/liveness/',
        project_views.HealthcheckLiveness.as_view(),
        name='healthcheck_liveness',
    ),
    path(
        'health-check/readiness/',
        project_views.HealthcheckReadiness.as_view(),
        name='healthcheck_readiness',
    ),
    path('admin/', admin.site.urls),
    path(
        'core/greetings/',
        core_views.GreetingsView.as_view(),
        name='core_greetings',
    ),
    path('core/links/', core_views.LinkViewSet, name='core_links'),
]
