from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class ExceptionMiddleware(MiddlewareMixin):
    """
    Customize the exceptions returned by views - instead of showing
    django's html response, customize it to be a json response
    (which is much better on an API's context).
    """

    def process_exception(self, request, exception):
        response = {'error': True, 'message': str(exception)}
        return JsonResponse(response, status=500)
