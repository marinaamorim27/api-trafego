from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from monitorizacao.views import SegmentoEstradaViewSet, LeituraViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from monitorizacao.views import RegistoPassagemBulkCreateView, passagens_ultimas_24h

router = routers.DefaultRouter()
router.register(r'segmentos', SegmentoEstradaViewSet)
router.register(r'leituras', LeituraViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API de Monitorização de Tráfego",
        default_version='v1',
        description="Dashboard de tráfego rodoviário",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path("api/passagens/bulk/", RegistoPassagemBulkCreateView.as_view()),
    path("api/passagens/ultimas24h/", passagens_ultimas_24h),
]
