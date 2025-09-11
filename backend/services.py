from sqlalchemy.orm import Session
from database import Product, ChatSession
from models import SlotMemory, ProductResponse
from typing import List, Dict, Any
from datetime import datetime
import json

class ProductService:
    def __init__(self, db: Session):
        self.db = db
    
    def search_products(self, memory: SlotMemory) -> List[ProductResponse]:
        """Search products based on filled memory slots"""
        query = self.db.query(Product)
        
        # Apply filters based on memory
        if memory.budget:
            query = query.filter(Product.price <= memory.budget)
            
        if memory.ram:
            query = query.filter(Product.ram >= memory.ram)
            
        if memory.storage:
            query = query.filter(Product.storage >= memory.storage)
            
        if memory.purpose:
            query = query.filter(Product.use_case.like(f"%{memory.purpose}%"))
            
        if memory.category:
            query = query.filter(Product.category == memory.category)
            
        if memory.brand_preference:
            query = query.filter(Product.brand.like(f"%{memory.brand_preference}%"))
            
        if memory.weight_preference:
            if memory.weight_preference == "light":
                query = query.filter(Product.weight <= 1.5)
            elif memory.weight_preference == "medium":
                query = query.filter(Product.weight.between(1.5, 2.5))
            elif memory.weight_preference == "heavy":
                query = query.filter(Product.weight >= 2.5)
                
        if memory.screen_size:
            if memory.screen_size == "small":
                query = query.filter(Product.screen_size <= 13)
            elif memory.screen_size == "medium":
                query = query.filter(Product.screen_size.between(14, 15))
            elif memory.screen_size == "large":
                query = query.filter(Product.screen_size >= 16)
        
        if memory.upgradability:
            if "ram" in memory.upgradability.lower():
                query = query.filter(Product.upgradable_ram == True)
            if "storage" in memory.upgradability.lower():
                query = query.filter(Product.upgradable_storage == True)
        
        # Order by relevance (you can customize this)
        query = query.order_by(Product.price.asc())
        
        # Limit results
        products = query.limit(5).all()
        
        return [ProductResponse(
            id=p.id,
            name=p.name,
            category=p.category,
            price=p.price,
            ram=p.ram,
            storage=p.storage,
            weight=p.weight,
            screen_size=p.screen_size,
            processor=p.processor,
            graphics=p.graphics,
            battery_life=p.battery_life,
            use_case=p.use_case,
            upgradable_ram=p.upgradable_ram,
            upgradable_storage=p.upgradable_storage,
            description=p.description,
            image_url=p.image_url,
            brand=p.brand
        ) for p in products]

class SessionService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_session(self, session_id: str) -> SlotMemory:
        """Get existing session memory or create new one"""
        session = self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        
        if session:
            return SlotMemory.parse_obj(json.loads(session.memory))
        else:
            # Create new session
            new_memory = SlotMemory()
            session = ChatSession(
                session_id=session_id,
                memory=json.dumps(new_memory.dict()),
                created_at=str(datetime.now()),
                updated_at=str(datetime.now())
            )
            self.db.add(session)
            self.db.commit()
            return new_memory
    
    def update_session(self, session_id: str, memory: SlotMemory):
        """Update session memory"""
        session = self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if session:
            session.memory = json.dumps(memory.dict())
            session.updated_at = str(datetime.now())
            self.db.commit()
    
    def should_recommend_products(self, memory: SlotMemory) -> bool:
        """Check if we have enough information to recommend products"""
        filled_slots = 0
        total_important_slots = 6
        
        if memory.budget is not None: filled_slots += 1
        if memory.purpose is not None: filled_slots += 1
        if memory.ram is not None: filled_slots += 1
        if memory.storage is not None: filled_slots += 1
        if len(memory.properties) > 0: filled_slots += 1
        if memory.performance_needs is not None: filled_slots += 1
        
        return filled_slots / total_important_slots >= 0.6  # 60% threshold
