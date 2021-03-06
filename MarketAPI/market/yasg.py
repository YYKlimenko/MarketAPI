from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .permissions import IsAdminOrReadOnly


schema_view = get_schema_view(
   openapi.Info(
      title="Market API",
      default_version='v1',
      description="Description API",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(IsAdminOrReadOnly,),
)

urlpatterns = [
   path('api/v1/swagger(<format>.json|.yaml)',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
   path('api/v1/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
]
