import logging

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django_celery_results.models import TaskResult
from mlplayground import celery_app

from .serializers import DQMIOCeleryTasksSerializer, InspectResponseBase, InspectInputSerializer, InspectResponseSerializer

logger = logging.getLogger(__name__)
inspect = celery_app.control.inspect()


class DQMIOCeleryTasksViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    You can see all ingested Runs metadata
    """
    queryset = TaskResult.objects.all().order_by("id")
    serializer_class = DQMIOCeleryTasksSerializer
    lookup_field = "task_id"

    @extend_schema(
        request=InspectInputSerializer,
        responses={200: InspectResponseSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=["get"],
        name="List received tasks waiting to start",
        url_path=r"queued",
        pagination_class=None
    )
    def check_queued_tasks(self, request):
        result = []
        for worker, tasks in inspect.reserved().items():
            for task in tasks:
                    result.append(InspectResponseBase(
                        id=task.get("id"),
                        name=task.get("name"),
                        queue=task.get("delivery_info", {}).get("routing_key"),
                        worker=worker
                    ))

        result = InspectResponseSerializer(result, many=True)
        return Response(result.data)


    @extend_schema(
        request=InspectInputSerializer,
        responses={200: InspectResponseSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=["get"],
        name="List started tasks",
        url_path=r"active",
        pagination_class=None
    )
    def check_active_tasks(self, request):
        result = []
        for worker, tasks in inspect.active().items():
            for task in tasks:
                    result.append(InspectResponseBase(
                        id=task.get("id"),
                        name=task.get("name"),
                        queue=task.get("delivery_info", {}).get("routing_key"),
                        worker=worker
                    ))

        result = InspectResponseSerializer(result, many=True)
        return Response(result.data)