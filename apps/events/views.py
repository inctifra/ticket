from django.views import View
from django.http import JsonResponse


class EventLaunchRequestView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({})
