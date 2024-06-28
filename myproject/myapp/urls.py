from django.urls import path
from .views import concatenate_email
from .views import base64_view
urlpatterns = [
    path('concatenate-email/', concatenate_email),
    path('base64/', base64_view, name='base64'),
]
