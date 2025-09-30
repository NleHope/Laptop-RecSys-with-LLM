from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SlotMemory(BaseModel):
    budget: Optional[float] = None
    ram: Optional[int] = None
    storage: Optional[int] = None
    purpose: Optional[str] = None
    properties: List[str] = []
    upgradability: Optional[str] = None  # "ram", "storage", "both", "none"
    category: Optional[str] = None  # laptop, smartphone, etc.
    brand_preference: Optional[str] = None
    screen_size: Optional[str] = None  # "small", "medium", "large"
    weight_preference: Optional[str] = None  # "light", "medium", "heavy"
    performance_needs: Optional[str] = None  # "basic", "medium", "high"

class ChatMessage(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    needs_more_info: bool
    recommended_products: List[Dict[str, Any]] = []

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    ram: Optional[int]
    storage: Optional[int]
    weight: Optional[float]
    screen_size: Optional[float]
    processor: Optional[str]
    graphics: Optional[str]
    battery_life: Optional[int]
    use_case: Optional[str]
    upgradable_ram: bool
    upgradable_storage: bool
    description: Optional[str]
    image_url: Optional[str]
    brand: Optional[str]
