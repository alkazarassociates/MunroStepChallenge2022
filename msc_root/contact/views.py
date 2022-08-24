from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, get_connection

from .forms import ContactForm

def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            send_mail(
                cd['subject'],
                cd.get('email', 'NO REPLY EMAIL') + "\n" + cd['message'],
                'teamstepchallenge2022@gmail.com',
                ['teamstepchallenge2022@gmail.com']
            )
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'contact/contact.html', {'form': form, 'submitted': submitted})