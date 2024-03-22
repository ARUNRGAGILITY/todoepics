# your_app/context_processors.py

from django.conf import settings

def get_site_info(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'BUILD_VERSION': settings.BUILD_VERSION,
        'BUILD_DESCRIPTION': settings.BUILD_DESCRIPTION,
        'COPYRIGHT_INFO': settings.COPYRIGHT_INFO,
    }
