from django.urls import path
from .views import siswa_handler

urlpatterns = [
    path('siswa/', siswa_handler, name='rev_siswa_handler'),  # Tanpa ID
    path('siswa/<int:siswa_id>/', siswa_handler, name='rev_siswa_handler_detail'),  # Dengan ID
]
