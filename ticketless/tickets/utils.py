from django.utils.text import slugify


def upload_event_image_path(instance, filename):
    return f"events/{slugify(instance.event.title)}/images/{filename}"
