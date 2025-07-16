from app import create_app, db
from app.models import Admin

app = create_app()
with app.app_context():
    email = "admin@email.com"
    password = "admin123"

    if not Admin.query.filter_by(email=email).first():
        admin = Admin(email=email)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin berhasil ditambahkan.")
    else:
        print("Admin sudah ada.")
