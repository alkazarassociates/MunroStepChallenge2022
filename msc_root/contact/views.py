from email.message import EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage, send_mail, get_connection

from .forms import ContactForm

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            email = EmailMessage(
                cd['subject'],
                'From ' + cd['yourname'] + '\n' + cd['message'],
                EMAIL_OUR_ADDRESS,  # From
                [EMAIL_OUR_ADDRESS] # to
            )
            if 'email' in cd:
                email.reply_to = [cd['email']]
            
            email.send()
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'contact/contact.html', {'form': form, 'submitted': submitted, 'our_email': settings.EMAIL_OUR_ADDRESS})