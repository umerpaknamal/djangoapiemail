from django.urls import path
from .views import concatenate_email
from . import views
urlpatterns = [
    path('concatenate-email/', concatenate_email),
    path('base64/', views.Base64View.as_view(), name='base64'),
]
