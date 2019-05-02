from django.urls import path, re_path
from mySite.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home_page_url'),
    path('attachment/<int:numb>/', AttachmentDetail.as_view(), name='attachment_detail_url'),
    path('next', pagination),
    path('previous', pagination),
]
