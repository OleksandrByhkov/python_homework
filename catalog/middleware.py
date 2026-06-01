import logging
import time

logger = logging.getLogger("catalog")


class RequestTimeLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(
            f"Path: {request.path} | Method: {request.method} | Time: {duration:.3f}s"
        )

        return response