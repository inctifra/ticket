from .forms import EventLaunchRequestForm


def load_core_context(request):
    return {"request_event_launch_form": EventLaunchRequestForm()}
