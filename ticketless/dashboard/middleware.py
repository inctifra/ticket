import contextlib


class UserProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        profile = None

        if request.user.is_authenticated:
            with contextlib.suppress(Exception):
                profile = request.user.profile
        request.profile = profile
        return self.get_response(request)
