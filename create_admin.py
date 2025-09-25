#!/usr/bin/env python3
"""Create admin user script."""

import asyncio
import uuid
from datetime import datetime

import asyncpg
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

async def create_admin():
    """Create admin user."""
    # Connect directly to PostgreSQL
    conn = await asyncpg.connect(
        host='localhost',
        port=5434,  # User management postgres port
        database='user_management',
        user='user_management_user',
        password='user_management_password'
    )
    
    try:
        # Check if admin user exists
        existing_user = await conn.fetchrow(
            "SELECT id FROM users WHERE email = $1", 
            'admin@example.com'
        )
        
        if existing_user:
            print('Admin user already exists!')
            return
            
        # Create admin user
        hashed_password = pwd_context.hash('password')
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        await conn.execute(
            """INSERT INTO users (id, email, first_name, last_name, hashed_password, 
               is_active, is_superuser, email_verified, created_at, updated_at)
               VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)""",
            user_id,
            'admin@example.com',
            'Admin',
            'User', 
            hashed_password,
            True,
            True,
            True,
            now,
            now
        )
        
        print('✅ Admin user created successfully!')
        print('Email: admin@example.com')
        print('Password: password')
        
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
