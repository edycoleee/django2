from django.test import TestCase, Client
from django.urls import reverse
from django.db import connection
import json

class SiswaAPITestCase(TestCase):
    
    def setUp(self):
        """Menyiapkan database sebelum setiap pengujian."""
        self.client = Client()

        # Buat tabel siswa jika belum ada
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS siswa (
                    id INTEGER PRIMARY KEY,  -- SQLite otomatis AUTO_INCREMENT
                    namaSiswa TEXT,
                    alamatSiswa TEXT
                )
            """)

        # Masukkan data dummy untuk pengujian (dilakukan dalam blok with yang berbeda)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO siswa (namaSiswa, alamatSiswa) VALUES ('Jane Doe', 'Jl. Sudirman') RETURNING id")
            self.siswa_id = cursor.fetchone()[0]
            #print({self.siswa_id})
    
    def test_create_siswa(self):
        """Test endpoint POST /siswa"""
        url = reverse('rev_siswa_handler')
        data = {"namaSiswa": "John Doe", "alamatSiswa": "Jl. Merdeka"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Siswa berhasil ditambahkan")
        self.assertIn("url", response_data)  # Cek apakah URL siswa ada dalam response

    def test_get_all_siswa(self):
        """Test endpoint GET /siswa"""
        url = reverse('rev_siswa_handler')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Daftar semua siswa")
        self.assertGreaterEqual(response_data["total"], 1)

    def test_get_siswa_by_id(self):
        """Test endpoint GET /siswa/<id>"""
        url = reverse('rev_siswa_handler_detail', args=[self.siswa_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Data siswa ditemukan")
        self.assertEqual(response_data["data"]["id"], self.siswa_id)

    def test_update_siswa(self):
        """Test endpoint PUT /siswa/<id>"""
        url = reverse('rev_siswa_handler_detail', args=[self.siswa_id])
        data = {"namaSiswa": "Jane Doe Updated", "alamatSiswa": "Jl. Sudirman No. 10"}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Siswa berhasil diperbarui")
        self.assertEqual(response_data["namaSiswa"], "Jane Doe Updated")

    def test_delete_siswa(self):
        """Test endpoint DELETE /siswa/<id>"""
        url = reverse('rev_siswa_handler_detail', args=[self.siswa_id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["message"], "Siswa berhasil dihapus")
        self.assertEqual(response_data["id"], self.siswa_id)

        # Cek apakah siswa benar-benar dihapus
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
