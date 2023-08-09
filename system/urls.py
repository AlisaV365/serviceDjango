from django.urls import path

from system.apps import SystemConfig
from system.views import home, MailingCreateView, MailingUpdateView, MailingDeleteView, ClientCreateView, \
    MessageCreateView, MailingListView, disable_mailing, MailingLogList, MailingMessagesList, ClientListView

app_name = SystemConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('update/<int:pk>', MailingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),
    path('clients/create', ClientCreateView.as_view(), name='create_client'),
    path('message/create', MessageCreateView.as_view(), name='create_message'),
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/disable/<int:pk>', disable_mailing, name='disable'),
    path('log/', MailingLogList.as_view(), name='log'),
    path('messages/', MailingMessagesList.as_view(), name='messages'),
    path('clients/', ClientListView.as_view(), name='clients')
]