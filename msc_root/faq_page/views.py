from django.shortcuts import render

from .models import FaqPage

def faq_view(request):
    text = FaqPage.objects.first()
    return render(request, 'faq_page/faq.html', {'text': text})
