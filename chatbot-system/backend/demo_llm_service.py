"""
Demo LLM Service for testing without OpenAI API
This uses simple rule-based extraction for demonstration purposes
"""

import json
import re
from typing import Dict, Any, List
from models import SlotMemory

class DemoLLMService:
    def __init__(self):
        # Define keywords for different slots
        self.budget_patterns = [
            r'under\s+\$?(\d+)',
            r'less\s+than\s+\$?(\d+)',
            r'\$(\d+)\s+budget',
            r'budget\s+of\s+\$?(\d+)',
            r'\$(\d+)'
        ]
        
        self.purpose_keywords = {
            'gaming': ['gaming', 'games', 'game', 'gamer'],
            'education': ['school', 'college', 'student', 'study', 'education', 'university', 'academic'],
            'business': ['work', 'office', 'business', 'professional', 'corporate'],
            'creative': ['design', 'creative', 'art', 'photo', 'video', 'editing'],
            'programming': ['programming', 'coding', 'development', 'software', 'developer']
        }
        
        self.property_keywords = {
            'thin': ['thin', 'slim', 'sleek'],
            'light': ['light', 'lightweight', 'portable'],
            'fast': ['fast', 'quick', 'speedy', 'high-performance'],
            'durable': ['durable', 'sturdy', 'robust', 'tough'],
            'powerful': ['powerful', 'high-end', 'performance']
        }
        
        self.ram_patterns = [
            r'(\d+)\s*gb\s+ram',
            r'(\d+)\s*gb\s+memory',
            r'ram.*?(\d+)\s*gb',
            r'memory.*?(\d+)\s*gb'
        ]
        
        self.storage_patterns = [
            r'(\d+)\s*gb\s+storage',
            r'(\d+)\s*gb\s+ssd',
            r'storage.*?(\d+)\s*gb',
            r'ssd.*?(\d+)\s*gb'
        ]
    
    def extract_information(self, user_message: str, current_memory: SlotMemory) -> SlotMemory:
        """Extract structured information from user message using simple rules"""
        message_lower = user_message.lower()
        updated_memory = current_memory.copy()
        
        # Extract budget
        if updated_memory.budget is None:
            for pattern in self.budget_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    try:
                        updated_memory.budget = float(match.group(1))
                        break
                    except:
                        pass
        
        # Extract purpose
        if updated_memory.purpose is None:
            for purpose, keywords in self.purpose_keywords.items():
                if any(keyword in message_lower for keyword in keywords):
                    updated_memory.purpose = purpose
                    break
        
        # Extract properties
        for prop, keywords in self.property_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                if prop not in updated_memory.properties:
                    updated_memory.properties.append(prop)
        
        # Extract RAM
        if updated_memory.ram is None:
            for pattern in self.ram_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    try:
                        updated_memory.ram = int(match.group(1))
                        break
                    except:
                        pass
        
        # Extract storage
        if updated_memory.storage is None:
            for pattern in self.storage_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    try:
                        updated_memory.storage = int(match.group(1))
                        break
                    except:
                        pass
        
        # Extract upgradability
        if 'upgrade' in message_lower:
            if 'ram' in message_lower:
                updated_memory.upgradability = 'ram'
            elif 'storage' in message_lower:
                updated_memory.upgradability = 'storage'
            else:
                updated_memory.upgradability = 'both'
        
        # Set default category
        if updated_memory.category is None:
            updated_memory.category = 'laptop'
        
        # Infer performance needs
        if updated_memory.performance_needs is None:
            if any(word in message_lower for word in ['gaming', 'creative', 'video', 'high-performance']):
                updated_memory.performance_needs = 'high'
            elif any(word in message_lower for word in ['basic', 'simple', 'email', 'web']):
                updated_memory.performance_needs = 'basic'
            else:
                updated_memory.performance_needs = 'medium'
        
        return updated_memory
    
    def generate_response(self, user_message: str, memory: SlotMemory, products: List[Dict] = None) -> str:
        """Generate response using templates"""
        
        # Calculate completion
        filled_slots = 0
        total_important_slots = 6
        
        if memory.budget is not None: filled_slots += 1
        if memory.purpose is not None: filled_slots += 1
        if memory.ram is not None: filled_slots += 1
        if memory.storage is not None: filled_slots += 1
        if len(memory.properties) > 0: filled_slots += 1
        if memory.performance_needs is not None: filled_slots += 1
        
        completion_percentage = filled_slots / total_important_slots
        
        if products:  # We have products to recommend
            intro = f"Great! Based on your preferences, I found {len(products)} laptop(s) that match your needs:\n\n"
            
            summaries = []
            for product in products:
                summary = f"✅ **{product['name']}** - ${product['price']:.2f}"
                if product.get('ram'):
                    summary += f" | {product['ram']}GB RAM"
                if product.get('storage'):
                    summary += f" | {product['storage']}GB Storage"
                if product.get('weight'):
                    summary += f" | {product['weight']}kg"
                summaries.append(summary)
            
            return intro + "\n".join(summaries) + "\n\nWould you like more details about any of these laptops?"
        
        else:  # Need more information
            responses = []
            
            if completion_percentage < 0.3:
                responses.append("Thanks for reaching out! I'd love to help you find the perfect laptop.")
            else:
                responses.append("Great! I'm getting a better understanding of what you need.")
            
            # Ask for specific missing information
            missing_info = []
            
            if memory.budget is None:
                missing_info.append("What's your budget range?")
            
            if memory.purpose is None:
                missing_info.append("What will you primarily use it for? (gaming, school, work, etc.)")
            
            if memory.performance_needs is None and not missing_info:
                missing_info.append("Do you need high performance or is basic performance fine?")
            
            if not memory.properties and len(missing_info) < 2:
                missing_info.append("Any preferences for portability, weight, or design?")
            
            if missing_info:
                if len(missing_info) == 1:
                    responses.append(missing_info[0])
                else:
                    responses.append("A few quick questions:")
                    for i, question in enumerate(missing_info[:2], 1):
                        responses.append(f"{i}. {question}")
            else:
                responses.append("I think I have enough information to find some options for you!")
            
            return " ".join(responses)

# Create a demo service instance
demo_llm_service = DemoLLMService()
