from app import app, db
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Create admin user if it doesn't exist
        from app import User
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123', method='sha256')
            )
            db.session.add(admin)
            db.session.commit()
            print("Created admin user with username 'admin' and password 'admin123'")
    
    # Run the application
    app.run(debug=True)
