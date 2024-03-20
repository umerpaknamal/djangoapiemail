from django.urls import path
from .views import concatenate_email

urlpatterns = [
    path('concatenate-email/', concatenate_email),
]
