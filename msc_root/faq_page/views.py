from django.conf import settings
from django.shortcuts import render

from .models import FaqPage

def faq_view(request):
    return render(request, 'faq_page/faq.html', {'faqs': FaqPage.objects.order_by('id'), 'phase': settings.CURRENT_PHASE})
