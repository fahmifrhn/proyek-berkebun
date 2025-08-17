from django.contrib import admin
from .models import Tanaman, CatatanPerawatan, Panen, Jadwal, Masalah

# Mendaftarkan setiap model ke situs admin
admin.site.register(Tanaman)
admin.site.register(CatatanPerawatan)
admin.site.register(Panen)
admin.site.register(Jadwal)
admin.site.register(Masalah)