from django.urls import path
from . import views

urlpatterns = [
    path('rotate_pdf/', views.rotate_pdf),
    path('rotate_pdf_with_attachment/', views.rotate_pdf_with_attachment),
]
