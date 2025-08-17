# kebun/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Halaman Utama
    path('', views.dashboard, name='dashboard'),
    
    # URL untuk halaman kalender
    path('kalender/', views.kalender_view, name='kalender'),

    # -- CRUD untuk Tanaman --
    path('tanaman/', views.TanamanListView.as_view(), name='tanaman-list'),
    path('tanaman/tambah/', views.TanamanCreateView.as_view(), name='tanaman-create'),
    path('tanaman/<int:pk>/', views.TanamanDetailView.as_view(), name='tanaman-detail'),
    path('tanaman/<int:pk>/update/', views.TanamanUpdateView.as_view(), name='tanaman-update'),
    path('tanaman/<int:pk>/delete/', views.TanamanDeleteView.as_view(), name='tanaman-delete'),
    
    # -- CRUD untuk Catatan Perawatan (Nested di dalam Tanaman) --
    path('tanaman/<int:tanaman_pk>/catatan/tambah/', views.CatatanPerawatanCreateView.as_view(), name='catatan-create'),
    path('catatan/<int:pk>/update/', views.CatatanPerawatanUpdateView.as_view(), name='catatan-update'),
    path('catatan/<int:pk>/delete/', views.CatatanPerawatanDeleteView.as_view(), name='catatan-delete'),

    # -- CRUD untuk Panen (Nested di dalam Tanaman) --
    path('tanaman/<int:tanaman_pk>/panen/tambah/', views.PanenCreateView.as_view(), name='panen-create'),
    path('panen/<int:pk>/update/', views.PanenUpdateView.as_view(), name='panen-update'),
    path('panen/<int:pk>/delete/', views.PanenDeleteView.as_view(), name='panen-delete'),

    # -- CRUD untuk Jadwal (Nested di dalam Tanaman) --
    path('tanaman/<int:tanaman_pk>/jadwal/tambah/', views.JadwalCreateView.as_view(), name='jadwal-create'),
    path('jadwal/<int:pk>/update/', views.JadwalUpdateView.as_view(), name='jadwal-update'),
    path('jadwal/<int:pk>/delete/', views.JadwalDeleteView.as_view(), name='jadwal-delete'),
    path('api/jadwal/<int:pk>/toggle-selesai/', views.toggle_jadwal_selesai, name='jadwal-toggle-selesai'),

    # -- CRUD untuk Masalah (Nested di dalam Tanaman) --
    path('tanaman/<int:tanaman_pk>/masalah/tambah/', views.MasalahCreateView.as_view(), name='masalah-create'),
    path('masalah/<int:pk>/update/', views.MasalahUpdateView.as_view(), name='masalah-update'),
    path('masalah/<int:pk>/delete/', views.MasalahDeleteView.as_view(), name='masalah-delete'),

    # Export
    path('panen/export/', views.export_panen_csv, name='export-panen-csv'),
    
    # URL untuk menyediakan data ke FullCalendar
    path('api/semua-jadwal/', views.semua_jadwal_json, name='semua-jadwal-json'),

]