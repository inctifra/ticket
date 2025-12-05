from django import template

from ticketless.dashboard.tenant.permissions import is_owner_or_manager

register = template.Library()


@register.inclusion_tag("tenants/templatetags/profile_header.html", takes_context=True)
def load_dashboard_header(context, extra_data=None):
    request = context["request"]
    return {
        "request": request,
        "user": request.user,
        "extra_data": extra_data,
    }


@register.filter
def is_owner_or_manager_filter(user):
    return is_owner_or_manager(user)
