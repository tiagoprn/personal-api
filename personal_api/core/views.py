import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.filters import UrlFilter
from core.models import Url
from core.serializers import UrlSerializer

logger = logging.getLogger(__name__)


class GreetingsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        content = {'message': f'Hello there, {user}!'}
        return Response(content)


class UrlViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = (
        Url.objects.all()
    )  # TODO: get by request user, using the model manager method
    serializer_class = UrlSerializer
    filterset_class = UrlFilter
    # TODO: pagination_class = StandardResultsSetPagination
