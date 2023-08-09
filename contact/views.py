from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


# from tasks import send_spam_email


class ContactView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
    template_name = 'contact.html'
