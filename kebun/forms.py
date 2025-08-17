# kebun/forms.py

from django import forms
from .models import CatatanPerawatan, Panen, Jadwal, Masalah
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Helper ini akan kita gunakan untuk semua form
class BaseFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.add_input(Submit('submit', 'Simpan', css_class='btn-success mt-3'))
        # Tombol Batal bisa ditambahkan di template jika perlu

class CatatanPerawatanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()

    class Meta:
        model = CatatanPerawatan
        fields = ['aktivitas', 'foto_perkembangan']
        widgets = {
            'aktivitas': forms.Textarea(attrs={'rows': 4}),
        }

class PanenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['jumlah'].help_text = 'Jumlah hasil panen (misal: dalam gram, kg, atau buah)'

    class Meta:
        model = Panen
        fields = ['tanggal_panen', 'jumlah', 'satuan', 'catatan']
        widgets = {
            'tanggal_panen': forms.DateInput(attrs={'type': 'date'}),
            'catatan': forms.Textarea(attrs={'rows': 4}),
        }

class JadwalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()

    class Meta:
        model = Jadwal
        fields = ['jenis_kegiatan', 'tanggal_jadwal', 'selesai']
        widgets = {
            'tanggal_jadwal': forms.DateInput(attrs={'type': 'date'}),
        }

class MasalahForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = BaseFormHelper()
        self.fields['deskripsi_masalah'].help_text = 'Jelaskan hama, penyakit, atau masalah lain yang ditemukan'
        self.fields['solusi_dicoba'].help_text = 'Tindakan apa yang sudah dilakukan untuk mengatasi masalah'

    class Meta:
        model = Masalah
        fields = ['tanggal_ditemukan', 'deskripsi_masalah', 'solusi_dicoba', 'berhasil']
        widgets = {
            'tanggal_ditemukan': forms.DateInput(attrs={'type': 'date'}),
            'deskripsi_masalah': forms.Textarea(attrs={'rows': 4}),
            'solusi_dicoba': forms.Textarea(attrs={'rows': 4}),
        }