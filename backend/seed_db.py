#!/usr/bin/env python3
"""
Database seeding script for the AI Chatbot system.
This script populates the database with sample products.
"""

import sys
import os
from sqlalchemy.orm import Session
from database import engine, get_db, Product

def seed_database():
    """Seed the database with sample products"""
    db = next(get_db())
    
    # Check if products already exist
    if db.query(Product).count() > 0:
        print("Database already has products. Skipping seeding.")
        return
    
    # Sample products data
    products = [
        {
            "name": "Premium Wireless Headphones",
            "description": "High-quality noise-cancelling headphones with 30-hour battery life",
            "price": 199.99,
            "category": "Audio",
            "ram": None,
            "storage": None,
            "weight": 0.3,
            "screen_size": None,
            "processor": None,
            "graphics": None,
            "battery_life": 30,
            "use_case": "Entertainment",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "AudioTech",
            "image_url": "https://example.com/headphones.jpg"
        },
        {
            "name": "Fitness Smartwatch",
            "description": "Waterproof fitness tracker with heart rate monitoring and GPS",
            "price": 149.99,
            "category": "Wearables",
            "ram": 1,
            "storage": 8,
            "weight": 0.05,
            "screen_size": 1.4,
            "processor": "ARM",
            "graphics": None,
            "battery_life": 168,
            "use_case": "Fitness",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "FitTech",
            "image_url": "https://example.com/smartwatch.jpg"
        },
        {
            "name": "Ultra-Slim Laptop",
            "description": "Lightweight laptop with 14-inch display and all-day battery life",
            "price": 899.99,
            "category": "Computers",
            "ram": 16,
            "storage": 512,
            "weight": 1.2,
            "screen_size": 14.0,
            "processor": "Intel Core i7",
            "graphics": "Integrated Intel Iris Xe",
            "battery_life": 10,
            "use_case": "Business",
            "upgradable_ram": True,
            "upgradable_storage": True,
            "brand": "TechBook",
            "image_url": "https://example.com/laptop.jpg"
        },
        {
            "name": "Smart Home Security Camera",
            "description": "Indoor/outdoor security camera with night vision and motion detection",
            "price": 79.99,
            "category": "Smart Home",
            "ram": 1,
            "storage": 16,
            "weight": 0.3,
            "screen_size": None,
            "processor": "ARM",
            "graphics": None,
            "battery_life": None,
            "use_case": "Security",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "SecureView",
            "image_url": "https://example.com/camera.jpg"
        },
        {
            "name": "Gaming Console",
            "description": "Next-generation gaming console with 4K graphics and 1TB storage",
            "price": 499.99,
            "category": "Gaming",
            "ram": 16,
            "storage": 1000,
            "weight": 4.5,
            "screen_size": None,
            "processor": "Custom AMD Zen 2",
            "graphics": "Custom RDNA 2",
            "battery_life": None,
            "use_case": "Gaming",
            "upgradable_ram": False,
            "upgradable_storage": True,
            "brand": "GameSphere",
            "image_url": "https://example.com/console.jpg"
        },
        {
            "name": "Professional DSLR Camera",
            "description": "High-end DSLR camera for professional photography",
            "price": 1299.99,
            "category": "Photography",
            "ram": 2,
            "storage": 64,
            "weight": 0.8,
            "screen_size": 3.2,
            "processor": "DIGIC X",
            "graphics": None,
            "battery_life": 5,
            "use_case": "Photography",
            "upgradable_ram": False,
            "upgradable_storage": True,
            "brand": "OptiView",
            "image_url": "https://example.com/dslr.jpg"
        },
        {
            "name": "Portable Bluetooth Speaker",
            "description": "Waterproof portable speaker with 360-degree sound",
            "price": 89.99,
            "category": "Audio",
            "ram": None,
            "storage": None,
            "weight": 0.4,
            "screen_size": None,
            "processor": None,
            "graphics": None,
            "battery_life": 20,
            "use_case": "Entertainment",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "SoundWave",
            "image_url": "https://example.com/speaker.jpg"
        },
        {
            "name": "Electric Standing Desk",
            "description": "Height-adjustable desk with memory settings",
            "price": 349.99,
            "category": "Furniture",
            "ram": None,
            "storage": None,
            "weight": 50.0,
            "screen_size": None,
            "processor": None,
            "graphics": None,
            "battery_life": None,
            "use_case": "Office",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "ErgoPro",
            "image_url": "https://example.com/desk.jpg"
        },
        {
            "name": "Robot Vacuum Cleaner",
            "description": "Smart vacuum with mapping technology and self-emptying bin",
            "price": 399.99,
            "category": "Smart Home",
            "ram": 1,
            "storage": 8,
            "weight": 3.5,
            "screen_size": None,
            "processor": "ARM",
            "graphics": None,
            "battery_life": 3,
            "use_case": "Home Cleaning",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "CleanTech",
            "image_url": "https://example.com/vacuum.jpg"
        },
        {
            "name": "Ergonomic Office Chair",
            "description": "Comfortable chair with lumbar support and adjustable features",
            "price": 249.99,
            "category": "Furniture",
            "ram": None,
            "storage": None,
            "weight": 20.0,
            "screen_size": None,
            "processor": None,
            "graphics": None,
            "battery_life": None,
            "use_case": "Office",
            "upgradable_ram": False,
            "upgradable_storage": False,
            "brand": "ComfortPro",
            "image_url": "https://example.com/chair.jpg"
        }
    ]
    
    # Add products to database
    for product_data in products:
        product = Product(**product_data)
        db.add(product)
    
    db.commit()
    print(f"Added {len(products)} sample products to database")

if __name__ == "__main__":
    seed_database()
