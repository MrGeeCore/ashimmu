from django.conf import settings


def site_name(request):
    return {'ASHIMMU_SITE_NAME': settings.ASHIMMU_SITE_NAME}
