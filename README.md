## DJANGO REST API >> REVERSE URL

### 1. GITHUB

```js
echo "# django2" >> README.md
git init
git add 
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/django2.git
git push -u origin main
```

### 2. BUAT VENV
```py
#buat folder dj-api2 >> buka dengan vscode
#create venv
python3 -m venv .venv
#activate venv
source .venv/bin/activate
#check python venv
which python
#deactivate venv
#deactivate
```

```py
#melanjutkan 
python3 -m pip install --upgrade pip
python3 -m pip --version
```

```py
pip install django djangorestframework

django-admin --version

django-admin startproject siswaapi .

python manage.py runserver

#Starting development server at http://127.0.0.1:8000/

```

### 3 Siswa API Specification

## 1. Create Siswa
### Endpoint
**POST** `api/siswa/`

### Request Body (JSON)
```json
{
  "namaSiswa": "John Doe",
  "alamatSiswa": "Jl. Merdeka"
}
```

### Response (201 Created)
```json
{
  "message": "Siswa berhasil ditambahkan",
  "url": "/siswa/1"
}
```

## 2. Get All Siswa
### Endpoint
**GET** `api/siswa/`

### Response (200 OK)
```json
{
  "message": "Daftar semua siswa",
  "total": 1,
  "data": [
    {
      "id": 1,
      "namaSiswa": "Jane Doe",
      "alamatSiswa": "Jl. Sudirman"
    }
  ]
}
```

## 3. Get Siswa by ID
### Endpoint
**GET** `api/siswa/{id}/`

### Response (200 OK)
```json
{
  "message": "Data siswa ditemukan",
  "data": {
    "id": 1,
    "namaSiswa": "Jane Doe",
    "alamatSiswa": "Jl. Sudirman"
  }
}
```

### Response (404 Not Found)
```json
{
  "message": "Siswa tidak ditemukan"
}
```

## 4. Update Siswa
### Endpoint
**PUT** `api/siswa/{id}/`

### Request Body (JSON)
```json
{
  "namaSiswa": "Jane Doe Updated",
  "alamatSiswa": "Jl. Sudirman No. 10"
}
```

### Response (200 OK)
```json
{
  "message": "Siswa berhasil diperbarui",
  "namaSiswa": "Jane Doe Updated",
  "alamatSiswa": "Jl. Sudirman No. 10"
}
```

### Response (404 Not Found)
```json
{
  "message": "Siswa tidak ditemukan"
}
```

## 5. Delete Siswa
### Endpoint
**DELETE** `/siswa/{id}/`

### Response (200 OK)
```json
{
  "message": "Siswa berhasil dihapus",
  "id": 1
}
```

### Response (404 Not Found)
```json
{
  "message": "Siswa tidak ditemukan"
}
```
=============================

### 4. DATABASE ORM

Secara default, Django akan membuat nama tabel di database berdasarkan nama aplikasi dan nama model dengan format:
`<nama_aplikasi>_<nama_model>`

```py
#/siswa/model.py
from django.db import models

class Siswa(models.Model):
    namaSiswa = models.CharField(max_length=100)
    alamatSiswa = models.TextField()

    class Meta:
        db_table = "tbl_siswa"  # Menentukan nama tabel di SQLite

```

```py
python3 manage.py makemigrations
python3 manage.py migrate
```

CEK DATA

```py
python manage.py dbshell

.tables
```

### 4. DATABASE NO ORM

```py
python3 manage.py dbshell
```

```sql
CREATE TABLE siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    namaSiswa TEXT NOT NULL,
    alamatSiswa TEXT NOT NULL
);


PRAGMA table_info(siswa);
```

### 5. SETTING

```py

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siswa',  # Tambahkan aplikasi siswa di sini
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### 6. URLS UTAMA

```py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('siswa.urls'))
]

```
### 7. URLS SISWA
```py
from django.urls import path
from .views import siswa_handler

urlpatterns = [
    path('siswa/', siswa_handler, name='rev_siswa_handler'),  # Tanpa ID
    path('siswa/<int:siswa_id>/', siswa_handler, name='rev_siswa_handler_detail'),  # Dengan ID
]

```

### 8. VIEWS SISWA
```py
from django.http import JsonResponse
from django.urls import reverse
from django.db import connection
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

def siswa_handler(request, siswa_id=None):
    if request.method == "POST":
        return create_siswa(request)
    elif request.method == "GET":
        return get_siswa_by_id(request, siswa_id) if siswa_id else get_all_siswa(request)
    elif request.method == "PUT" and siswa_id:
        return update_siswa(request, siswa_id)
    elif request.method == "DELETE" and siswa_id:
        return delete_siswa(request, siswa_id)
    return JsonResponse({"error": "Metode tidak diizinkan"}, status=405)

@csrf_exempt
def create_siswa(request):
    try:
        data = JSONParser().parse(request)
        nama, alamat = data.get("namaSiswa"), data.get("alamatSiswa")
        if not nama or not alamat:
            return JsonResponse({"error": "Nama dan alamat harus diisi"}, status=400)
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO siswa (namaSiswa, alamatSiswa) VALUES (%s, %s) RETURNING id",
                [nama, alamat]
            )
            siswa_id = cursor.fetchone()[0]
        
        return JsonResponse({
            "message": "Siswa berhasil ditambahkan",
            "id": siswa_id,
            "namaSiswa": nama,
            "alamatSiswa": alamat,
            "url": reverse('rev_siswa_handler')
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_all_siswa(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, namaSiswa, alamatSiswa FROM siswa")
            siswa_list = cursor.fetchall()
        
        data = [
            {"id": row[0], "namaSiswa": row[1], "alamatSiswa": row[2], "url": reverse('rev_siswa_handler')}
            for row in siswa_list
        ]
        
        return JsonResponse({"message": "Daftar semua siswa", "total": len(data), "data": data}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_siswa_by_id(request, siswa_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, namaSiswa, alamatSiswa FROM siswa WHERE id = %s", [siswa_id])
            row = cursor.fetchone()
        
        if not row:
            return JsonResponse({"message": "Siswa tidak ditemukan"}, status=404)
        
        return JsonResponse({
            "message": "Data siswa ditemukan",
            "data": {"id": row[0], "namaSiswa": row[1], "alamatSiswa": row[2], "url": reverse('rev_siswa_handler_detail', args=[siswa_id])}
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_siswa(request, siswa_id):
    try:
        data = JSONParser().parse(request)
        nama, alamat = data.get("namaSiswa"), data.get("alamatSiswa")
        if not nama or not alamat:
            return JsonResponse({"error": "Nama dan alamat harus diisi"}, status=400)
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM siswa WHERE id = %s", [siswa_id])
            if not cursor.fetchone():
                return JsonResponse({"message": "Siswa tidak ditemukan"}, status=404)
            
            cursor.execute("UPDATE siswa SET namaSiswa = %s, alamatSiswa = %s WHERE id = %s", [nama, alamat, siswa_id])
        
        return JsonResponse({
            "message": "Siswa berhasil diperbarui",
            "id": siswa_id,
            "namaSiswa": nama,
            "alamatSiswa": alamat,
            "url": reverse('rev_siswa_handler_detail', args=[siswa_id])
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_siswa(request, siswa_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM siswa WHERE id = %s", [siswa_id])
            if not cursor.fetchone():
                return JsonResponse({"message": "Siswa tidak ditemukan"}, status=404)
            
            cursor.execute("DELETE FROM siswa WHERE id = %s", [siswa_id])
        
        return JsonResponse({"message": "Siswa berhasil dihapus", "id": siswa_id}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

```
### 9. TEST SISWA
```py
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

```
### 10. REQUEST REST

```js

### 1. CREATE 
POST http://localhost:8000/api/siswa/ 
content-type: application/json

{
"namaSiswa": "Silmi", "alamatSiswa": "Jl. Merdeka12"
}

### 2. GET ALL
 GET http://localhost:8000/api/siswa/ HTTP/1.1

### 3. GET BY ID
 GET http://localhost:8000/api/siswa/1/ HTTP/1.1

### 4. DELETE BY ID
 DELETE http://localhost:8000/api/siswa/2/ HTTP/1.1

### 5. UPDATE BY ID
 PUT http://localhost:8000/api/siswa/3/ 
content-type: application/json

{
"namaSiswa": "John Doe12 UPDATE", "alamatSiswa": "Jl. Merdeka12"
}

```