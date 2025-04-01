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
