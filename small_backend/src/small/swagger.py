from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Skif&Trade",
      default_version='v1',
      description="Restfull api for small bots",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="ZIZ INC. Resident for ```AstanaHub```"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]