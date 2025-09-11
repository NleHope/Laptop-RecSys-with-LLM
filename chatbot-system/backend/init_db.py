#!/usr/bin/env python3
"""
Database initialization script for the AI Chatbot system.
Run this script to create tables and seed with sample data.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_tables
from seed_db import seed_database

def main():
    print("🤖 Initializing AI Chatbot Database...")
    
    # Create database tables
    print("📊 Creating database tables...")
    create_tables()
    print("✅ Database tables created successfully!")
    
    # Seed with sample data
    print("🌱 Seeding database with sample products...")
    seed_database()
    print("✅ Database seeded successfully!")
    
    print("🎉 Database initialization complete!")
    print("🚀 You can now start the backend server with: python main.py")

if __name__ == "__main__":
    main()
