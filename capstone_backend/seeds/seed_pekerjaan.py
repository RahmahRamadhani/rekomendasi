from app import create_app, db
from app.models import Pekerjaan
from datetime import date, timedelta
import random

app = create_app()

# List data random
gaji_list = [
    "Rp5.000.000 - Rp8.000.000",
    "Rp7.000.000 - Rp12.000.000",
    "Rp10.000.000 - Rp15.000.000",
    "Rp15.000.000 - Rp25.000.000",
    "Rp20.000.000+"
]

tipe_pekerjaan_list = ["Full-time", "Part-time", "Remote", "Contract", "Internship"]

syarat_list = [
    "Minimal S1 di bidang terkait, pengalaman 1-3 tahun, mampu bekerja secara tim.",
    "Menguasai teknologi terbaru, komunikasi baik, fresh graduate dipersilakan melamar.",
    "Pengalaman minimal 2 tahun di bidang relevan, sertifikasi menjadi nilai tambah.",
    "Kemampuan analisis kuat, terbiasa dengan deadline, kreatif dan inovatif.",
    "Minimal D3/S1, mampu berbahasa Inggris, memiliki portfolio proyek."
]

benefit_list = [
    "BPJS Kesehatan, Bonus Tahunan, Work From Home.",
    "Asuransi Karyawan, Tunjangan Transportasi, Laptop disediakan.",
    "Fleksibel jam kerja, Cuti tambahan, Pelatihan dan pengembangan karir.",
    "Bonus project, Tunjangan makan, Lingkungan kerja startup.",
    "Jaminan kesehatan lengkap, Tunjangan anak, Dana pensiun."
]

# Jalankan dalam konteks aplikasi Flask
with app.app_context():
    pekerjaan_list = Pekerjaan.query.all()

    for pekerjaan in pekerjaan_list:
        updated = False

        if not pekerjaan.gaji:
            pekerjaan.gaji = random.choice(gaji_list)
            updated = True
        if not pekerjaan.tipe_pekerjaan:
            pekerjaan.tipe_pekerjaan = random.choice(tipe_pekerjaan_list)
            updated = True
        if not pekerjaan.tanggal_ditutup:
            pekerjaan.tanggal_ditutup = date.today() + timedelta(days=random.randint(7, 60))
            updated = True
        if not pekerjaan.syarat:
            pekerjaan.syarat = random.choice(syarat_list)
            updated = True
        if not pekerjaan.benefit:
            pekerjaan.benefit = random.choice(benefit_list)
            updated = True
        if not pekerjaan.link_apply:
            pekerjaan.link_apply = f"https://jobportal.example.com/apply/{pekerjaan.id}"
            updated = True

        if updated:
            print(f"✅ Pekerjaan ID {pekerjaan.id} ({pekerjaan.nama_pekerjaan}) berhasil diupdate.")

    db.session.commit()
    print("🎉 Semua data pekerjaan yang kosong berhasil diupdate dengan random data!")
