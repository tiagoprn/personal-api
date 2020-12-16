import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class GreetingsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        content = {'message': f'Hello there, {user}!'}
        return Response(content)
