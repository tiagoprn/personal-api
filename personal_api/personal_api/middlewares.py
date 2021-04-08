from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class ExceptionMiddleware(MiddlewareMixin):
    """
    Customize the exceptions returned by views - instead of showing
    django's html response, customize it to be a json response
    (which is much better on an API's context).
    """

    def process_exception(self, request, exception):
        frame = str(exception.__traceback__.tb_frame)
        locals_context = str(exception.__traceback__.tb_frame.f_locals)
        locals_context = f'[{locals_context[1:][:-1]}]'
        response = {
            'error': True,
            'message': str(exception),
            'frame': frame,
            'locals_context': locals_context,
        }
        return JsonResponse(response, status=500)
