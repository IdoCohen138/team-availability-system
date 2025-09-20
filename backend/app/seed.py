import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from .models import User
from .auth import hash_password


def load_seed_users():
    """Load seed users from configuration file."""
    config_file = os.getenv("SEED_USERS_FILE")
    if config_file and Path(config_file).exists():
        with open(config_file, 'r') as f:
            users = json.load(f)
            return users
    print("WARNING: No seed users configuration found!")
    print(f"DEBUG: SEED_USERS_FILE env var: {config_file}")
    print(f"DEBUG: File exists: {Path(config_file).exists() if config_file else 'N/A'}")
    print("Please create a seed_users.json file or set SEED_USERS_FILE environment variable.")
    print("Example seed_users.json:")
    print('''[
          {
          "username": "admin",
          "full_name": "Admin User",
          "password": "admin123", 
          "status": "Working"
          }
          ]''')
    return []


def run(db: Session):
    print("DEBUG: Starting seed process...")
    user_count = db.query(User).count()
    print(f"DEBUG: Current user count in database: {user_count}")
    
    if user_count > 0:
        print("DEBUG: Database already has users, skipping seed")
        return
    
    seed_users = load_seed_users()
    if not seed_users:
        print("DEBUG: No seed users to add")
        return
        
    print(f"DEBUG: Adding {len(seed_users)} users to database")
    for user_data in seed_users:
        print(f"DEBUG: Adding user: {user_data['username']}")
        db.add(User(
            username=user_data["username"],
            full_name=user_data["full_name"],
            password_hash=hash_password(user_data["password"]),
            status=user_data["status"]
        ))
    
    try:
        db.commit()
        print("DEBUG: Successfully committed seed users to database")
    except Exception as e:
        print(f"DEBUG: Error committing seed users: {e}")
        db.rollback()
        raise