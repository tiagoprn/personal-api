import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from core.filters import LinkFilter
from core.models import Link
from core.serializers import LinkSerializer

logger = logging.getLogger(__name__)


class GreetingsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        content = {'message': f'Hello there, {user}!'}
        return Response(content)


class LinkViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LinkSerializer
    filterset_class = LinkFilter

    def get_queryset(self):
        # user_id = self.request.query_params.get("user_id", None)
        user = self.request.user
        return Link.objects.from_user(user=user)
