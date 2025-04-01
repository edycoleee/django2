#/siswa/model.py
from django.db import models

class Siswa(models.Model):
    namaSiswa = models.CharField(max_length=100)
    alamatSiswa = models.TextField()

    class Meta:
        db_table = "tbl_siswa"  # Menentukan nama tabel di SQLite
