from django.http import HttpResponseForbidden


def owner_or_manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        tenant = request.tenant
        user = request.user

        if user.id in (tenant.owner_id, tenant.manager_id):
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            "Action allowed only for the tenant manager or owner."
        )

    return wrapper


def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        tenant = request.tenant
        user = request.user

        if user.id == tenant.manager_id:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            "The action is only permitted for the tenant manager."
        )

    return wrapper


def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        tenant = request.tenant
        user = request.user

        if user.id == tenant.owner_id:
            return view_func(request, *args, **kwargs)

        return HttpResponseForbidden(
            "The action is only permitted for the tenant owner."
        )

    return wrapper
