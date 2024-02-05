from django.urls import include, path, re_path
from django.conf import settings
from dqmio_celery_tasks.routers import router as dqmio_celery_tasks_router
from dqmio_etl.routers import router as dqmio_etl_router
from dqmio_file_indexer.routers import router as dqmio_file_indexer_router
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from react_frontend.views import serve_react

router = routers.DefaultRouter()
router.registry.extend(dqmio_file_indexer_router.registry)
router.registry.extend(dqmio_etl_router.registry)
router.registry.extend(dqmio_celery_tasks_router.registry)

urlpatterns = [
    path(r"api/v1/", include(router.urls), name="api-v1"),
    path(r"api/v1/schema", SpectacularAPIView.as_view(), name="schema-v1"),
    path(
        r"api/v1/swagger",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-v1",
    ),
    re_path(r"^(?P<path>.*)$", serve_react, {"document_root": settings.REACT_APP_BUILD_PATH}),
]
