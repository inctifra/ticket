from django.http import JsonResponse
from django.views import View


class EventLaunchRequestView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({})
