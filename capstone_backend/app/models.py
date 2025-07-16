from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    email = db.Column(db.String(255))
    jenis_kelamin = db.Column(db.Text)
    prodi = db.Column(db.String(255))
    jurusan = db.Column(db.String(255))
    minat = db.Column(db.Text)
    skill = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rekomendasi = db.relationship('HasilRekomendasi', backref='user', lazy=True)

class Pekerjaan(db.Model):
    __tablename__ = 'pekerjaan'

    id = db.Column(db.Integer, primary_key=True)
    nama_pekerjaan = db.Column(db.String(255))
    perusahaan = db.Column(db.String(255))
    lokasi = db.Column(db.String(255))
    deskripsi = db.Column(db.Text)
    gaji = db.Column(db.String(100))  # baru
    tipe_pekerjaan = db.Column(db.String(50))  # baru
    tanggal_ditutup = db.Column(db.Date)  # baru
    syarat = db.Column(db.Text)  # baru
    benefit = db.Column(db.Text)  # baru
    link_apply = db.Column(db.Text) # baru
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rekomendasi = db.relationship('HasilRekomendasi', backref='pekerjaan', lazy=True)

class HasilRekomendasi(db.Model):
    __tablename__ = 'hasil_rekomendasi'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pekerjaan_id = db.Column(db.Integer, db.ForeignKey('pekerjaan.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



