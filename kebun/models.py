from django.db import models
from django.urls import reverse

# Model utama untuk setiap tanaman [cite: 3]
class Tanaman(models.Model):
    # Mendefinisikan pilihan untuk status pertumbuhan
    STATUS_PERTUMBUHAN = [
        ('Benih', 'Benih'),
        ('Berkecambah', 'Berkecambah'),
        ('Muda', 'Muda'),
        ('Dewasa', 'Dewasa'),
        ('Berbunga', 'Berbunga'),
        ('Berbuah', 'Berbuah'),
        ('Siap Panen', 'Siap Panen'),
    ]

    nama = models.CharField(max_length=100, help_text="Contoh: Tomat, Cabai, Kangkung")
    varietas = models.CharField(max_length=100, blank=True, help_text="Contoh: Cherry, Rawit, Bangkok")
    lokasi_tanam = models.CharField(max_length=100, blank=True, help_text="Contoh: Pot A1, Polybag di teras")
    tanggal_tanam = models.DateField()
    catatan_kebutuhan = models.TextField(blank=True, help_text="Contoh: Butuh sinar matahari penuh, siram 2x sehari")
    status_pertumbuhan = models.CharField(max_length=20, choices=STATUS_PERTUMBUHAN, default='Benih')

    def __str__(self):
        return f"{self.nama} ({self.varietas})"

    def get_absolute_url(self):
        return reverse('tanaman-detail', kwargs={'pk': self.pk})

# Model untuk mencatat perawatan harian 
class CatatanPerawatan(models.Model):
    tanaman = models.ForeignKey(Tanaman, on_delete=models.CASCADE, related_name='catatan_perawatan')
    tanggal = models.DateTimeField(auto_now_add=True)
    aktivitas = models.TextField(help_text="Contoh: Menyiram, memberi pupuk NPK, menyemprot pestisida nabati")
    foto_perkembangan = models.ImageField(upload_to='foto_tanaman/', blank=True, null=True)

    class Meta:
        ordering = ['-tanggal']

    def __str__(self):
        return f"Perawatan {self.tanaman.nama} pada {self.tanggal.strftime('%d-%m-%Y')}"

# Model untuk mencatat hasil panen [cite: 6]
class Panen(models.Model):
    tanaman = models.ForeignKey(Tanaman, on_delete=models.CASCADE, related_name='hasil_panen')
    tanggal_panen = models.DateField()
    jumlah = models.DecimalField(max_digits=10, decimal_places=2, help_text="Jumlah hasil panen (misal: dalam gram, kg, atau buah)")
    satuan = models.CharField(max_length=20, default='gram')
    catatan = models.TextField(blank=True)

    class Meta:
        ordering = ['-tanggal_panen']

    def __str__(self):
        return f"Panen {self.jumlah} {self.satuan} dari {self.tanaman.nama}"

# Model untuk jadwal dan pengingat 
class Jadwal(models.Model):
    JENIS_KEGIATAN = [
        ('Penyiraman', 'Penyiraman'),
        ('Pemupukan', 'Pemupukan'),
        ('Lainnya', 'Lainnya'),
    ]
    tanaman = models.ForeignKey(Tanaman, on_delete=models.CASCADE, related_name='jadwal_kegiatan')
    jenis_kegiatan = models.CharField(max_length=20, choices=JENIS_KEGIATAN)
    tanggal_jadwal = models.DateField()
    selesai = models.BooleanField(default=False)

    class Meta:
        ordering = ['tanggal_jadwal']

    def __str__(self):
        return f"{self.jenis_kegiatan} untuk {self.tanaman.nama} pada {self.tanggal_jadwal}"

# Model untuk mencatat masalah seperti hama atau penyakit [cite: 7]
class Masalah(models.Model):
    tanaman = models.ForeignKey(Tanaman, on_delete=models.CASCADE, related_name='catatan_masalah')
    tanggal_ditemukan = models.DateField()
    deskripsi_masalah = models.TextField(help_text="Jelaskan hama, penyakit, atau masalah lain yang ditemukan")
    solusi_dicoba = models.TextField(blank=True, help_text="Tindakan apa yang sudah dilakukan untuk mengatasi masalah")
    berhasil = models.BooleanField(default=False)

    def __str__(self):
        return f"Masalah pada {self.tanaman.nama} ({self.tanggal_ditemukan})"