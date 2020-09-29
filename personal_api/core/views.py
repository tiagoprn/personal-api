import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

# pylint: disable=unused-argument,expression-not-assigned
class Healthcheck(APIView):
    permission_classes = ()

    def get(self, request):
        try:
            # TODO: Do a query to a model here to assert the database
            # connection is working.
            return Response(
                {
                    'status': 'OK',
                    'services': {'database': 'OK', 'backend': 'OK'},
                },
                status=status.HTTP_200_OK,
            )
        except BaseException:
            logger.exception('An exception occurred.')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GreetingsView(APIView):
    permission_classes = IsAuthenticated

    def get(self, request):
        content = {'message': 'Hello there!'}
        return Response(content)
