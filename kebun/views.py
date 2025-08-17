# kebun/views.py
import csv

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.views.decorators.http import require_POST
from .forms import CatatanPerawatanForm, JadwalForm, MasalahForm, PanenForm
from .models import CatatanPerawatan, Jadwal, Masalah, Panen, Tanaman
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
import datetime

# --- Dashboard & Export ---
def dashboard(request):
    # --- Data untuk Statistik Cepat (Sudah ada) ---
    jumlah_tanaman_aktif = Tanaman.objects.exclude(status_pertumbuhan='Siap Panen').count()
    panen_terbaru = Panen.objects.all()[:5]
    jadwal_mendatang = Jadwal.objects.filter(selesai=False).order_by('tanggal_jadwal')[:5]

    # --- 1. Persiapan Data untuk Grafik Panen per Bulan ---
    panen_per_bulan = Panen.objects.annotate(
        bulan=TruncMonth('tanggal_panen')
    ).values('bulan').annotate(
        total_panen=Sum('jumlah')
    ).order_by('bulan')
    # Format data agar bisa dibaca Chart.js
    labels_panen = [item['bulan'].strftime('%b %Y') for item in panen_per_bulan]
    data_panen = [float(item['total_panen']) for item in panen_per_bulan]

    # --- 2. Persiapan Data untuk Grafik Status Tanaman ---
    status_tanaman = Tanaman.objects.values(
        'status_pertumbuhan'
    ).annotate(
        jumlah=Count('id')
    ).order_by('status_pertumbuhan')
        
    # Format data
    labels_status = [item['status_pertumbuhan'] for item in status_tanaman]
    data_status = [item['jumlah'] for item in status_tanaman]

    context = {
        'jumlah_tanaman': jumlah_tanaman_aktif,
        'panen_terbaru': panen_terbaru,
        'jadwal_mendatang': jadwal_mendatang,
        # Kirim data grafik ke template
        'labels_panen': labels_panen,
        'data_panen': data_panen,
        'labels_status': labels_status,
        'data_status': data_status,
    }
    return render(request, 'kebun/dashboard.html', context)

def export_panen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="laporan_panen.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nama Tanaman', 'Varietas', 'Tanggal Panen', 'Jumlah', 'Satuan'])
    semua_panen = Panen.objects.select_related('tanaman').all()
    for panen in semua_panen:
        writer.writerow([panen.tanaman.nama, panen.tanaman.varietas, panen.tanggal_panen, panen.jumlah, panen.satuan])
    return response

def kalender_view(request):
    return render(request, 'kebun/kalender.html')

# --- Mixin untuk Nested Views ---
# Mixin ini membantu kita mendapatkan objek Tanaman induk untuk view Create
class TanamanNestedObjectMixin:
    def form_valid(self, form):
        # Otomatis hubungkan objek baru dengan Tanaman induknya
        tanaman = get_object_or_404(Tanaman, pk=self.kwargs['tanaman_pk'])
        form.instance.tanaman = tanaman
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Kirim info Tanaman induk ke template
        context = super().get_context_data(**kwargs)
        context['tanaman'] = get_object_or_404(Tanaman, pk=self.kwargs['tanaman_pk'])
        return context

# --- CRUD Views untuk Tanaman ---
class TanamanListView(ListView):
    model = Tanaman
    context_object_name = 'daftar_tanaman'
    template_name = 'kebun/tanaman_list.html'

class TanamanDetailView(DetailView):
    model = Tanaman
    context_object_name = 'tanaman'
    template_name = 'kebun/tanaman_detail.html'

class TanamanCreateView(CreateView):
    model = Tanaman
    fields = ['nama', 'varietas', 'lokasi_tanam', 'tanggal_tanam', 'catatan_kebutuhan', 'status_pertumbuhan']
    template_name = 'kebun/tanaman_form.html'
    success_url = reverse_lazy('tanaman-list')

class TanamanUpdateView(UpdateView):
    model = Tanaman
    fields = ['nama', 'varietas', 'lokasi_tanam', 'tanggal_tanam', 'catatan_kebutuhan', 'status_pertumbuhan']
    template_name = 'kebun/tanaman_form.html'
    # success_url akan otomatis ke halaman detail tanaman yang diupdate

class TanamanDeleteView(DeleteView):
    model = Tanaman
    template_name = 'kebun/konfirmasi_hapus.html'
    success_url = reverse_lazy('tanaman-list')

# --- CRUD Views untuk CatatanPerawatan ---
class CatatanPerawatanCreateView(TanamanNestedObjectMixin, CreateView):
    model = CatatanPerawatan
    form_class = CatatanPerawatanForm
    template_name = 'kebun/catatanperawatan_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.kwargs['tanaman_pk']})

class CatatanPerawatanUpdateView(UpdateView):
    model = CatatanPerawatan
    form_class = CatatanPerawatanForm
    template_name = 'kebun/catatanperawatan_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

class CatatanPerawatanDeleteView(DeleteView):
    model = CatatanPerawatan
    template_name = 'kebun/konfirmasi_hapus.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

# --- CRUD Views untuk Panen ---
class PanenCreateView(TanamanNestedObjectMixin, CreateView):
    model = Panen
    form_class = PanenForm
    template_name = 'kebun/panen_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.kwargs['tanaman_pk']})

class PanenUpdateView(UpdateView):
    model = Panen
    form_class = PanenForm
    template_name = 'kebun/panen_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

class PanenDeleteView(DeleteView):
    model = Panen
    template_name = 'kebun/konfirmasi_hapus.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

# --- CRUD Views untuk Jadwal ---
class JadwalCreateView(TanamanNestedObjectMixin, CreateView):
    model = Jadwal
    form_class = JadwalForm
    template_name = 'kebun/jadwal_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.kwargs['tanaman_pk']})
        
class JadwalUpdateView(UpdateView):
    model = Jadwal
    form_class = JadwalForm
    template_name = 'kebun/jadwal_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

class JadwalDeleteView(DeleteView):
    model = Jadwal
    template_name = 'kebun/konfirmasi_hapus.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

# --- CRUD Views untuk Masalah ---
class MasalahCreateView(TanamanNestedObjectMixin, CreateView):
    model = Masalah
    form_class = MasalahForm
    template_name = 'kebun/masalah_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.kwargs['tanaman_pk']})

class MasalahUpdateView(UpdateView):
    model = Masalah
    form_class = MasalahForm
    template_name = 'kebun/masalah_form.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})

class MasalahDeleteView(DeleteView):
    model = Masalah
    template_name = 'kebun/konfirmasi_hapus.html'
    def get_success_url(self):
        return reverse_lazy('tanaman-detail', kwargs={'pk': self.object.tanaman.pk})
    
def semua_jadwal_json(request):
    """
    View ini menyediakan data semua objek Jadwal dalam format JSON
    yang bisa dibaca oleh FullCalendar.
    """
    semua_jadwal = Jadwal.objects.all()
    
    event_list = []
    for jadwal in semua_jadwal:
        event_list.append({
            'title': f"{jadwal.jenis_kegiatan} - {jadwal.tanaman.nama}",
            'start': jadwal.tanggal_jadwal.strftime("%Y-%m-%d"),
            'url': jadwal.tanaman.get_absolute_url(),
            'color': '#28a745' if jadwal.jenis_kegiatan == 'Penyiraman' else '#17a2b8'
        })
        
    return JsonResponse(event_list, safe=False)

@require_POST
def toggle_jadwal_selesai(request, pk):
    try:
        jadwal = get_object_or_404(Jadwal, pk=pk)
        
        # Logika untuk membalik status (dari True ke False, atau sebaliknya)
        jadwal.selesai = not jadwal.selesai
        jadwal.save()
        
        # Kirim kembali status baru dalam format JSON
        return JsonResponse({'status': 'ok', 'selesai': jadwal.selesai})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)