"""Create admin user script."""

import asyncio
import uuid
from datetime import datetime
from sqlalchemy import text
from app.core.database import engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def create_admin():
    """Create admin user."""
    async with engine.begin() as conn:
        # Check if admin user exists
        result = await conn.execute(
            text("SELECT id FROM users WHERE email = :email"), 
            {"email": 'admin@example.com'}
        )
        existing_user = result.fetchone()
        
        if existing_user:
            print('Admin user already exists!')
            return
            
        # Create admin user
        hashed_password = pwd_context.hash('password')
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        await conn.execute(
            text("""INSERT INTO users (id, email, first_name, last_name, hashed_password, 
                    is_active, is_superuser, email_verified, created_at, updated_at)
                    VALUES (:id, :email, :first_name, :last_name, :hashed_password, 
                    :is_active, :is_superuser, :email_verified, :created_at, :updated_at)"""),
            {
                "id": user_id,
                "email": 'admin@example.com',
                "first_name": 'Admin',
                "last_name": 'User', 
                "hashed_password": hashed_password,
                "is_active": True,
                "is_superuser": True,
                "email_verified": True,
                "created_at": now,
                "updated_at": now
            }
        )
        
        print('✅ Admin user created successfully!')
        print('Email: admin@example.com')
        print('Password: password')

if __name__ == "__main__":
    asyncio.run(create_admin())
