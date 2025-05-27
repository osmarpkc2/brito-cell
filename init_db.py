from app import app, db, User
import os

def init_db():
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123', method='sha256')
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()
    print("Database initialization complete.")
