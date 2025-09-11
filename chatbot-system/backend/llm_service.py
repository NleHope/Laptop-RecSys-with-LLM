import google.generativeai as genai
import json
import re
from typing import Dict, Any, List
from models import SlotMemory
import os
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("Successfully initialized Google Gemini API")
            except Exception as e:
                print(f"Error initializing Google Gemini API: {e}")
                self.model = None
        else:
            print("No Google API key found")
            self.model = None
        
    def extract_information(self, user_message: str, current_memory: SlotMemory) -> SlotMemory:
        """Extract structured information from user message and update slot memory"""
        
        system_prompt = f"""
You are an information extraction assistant for a laptop recommendation system. 
Extract relevant information from the user's message and update the current memory state.

Current memory state: {current_memory.dict()}

From the user's message, extract and update any of these fields:
- budget: numerical value in dollars (e.g., 1000, 1500)
- ram: RAM amount in GB (e.g., 8, 16, 32)
- storage: storage in GB (e.g., 256, 512, 1000)
- purpose: use case (education, gaming, business, creative, programming, general)
- properties: list of desired properties (thin, light, portable, powerful, fast, durable)
- upgradability: what they want to upgrade (ram, storage, both, none)
- category: product category (laptop, smartphone, tablet)
- brand_preference: preferred brand if mentioned
- screen_size: size preference (small=13 inch or less, medium=14-15 inch, large=16+ inch)
- weight_preference: weight preference (light=under 1.5kg, medium=1.5-2.5kg, heavy=over 2.5kg)
- performance_needs: performance level (basic, medium, high)

Return ONLY a JSON object with the updated memory state. If a field is not mentioned, keep the current value.
Do not include any explanations, just the JSON.

User message: "{user_message}"
"""
        
        try:
            if not self.model:
                return current_memory
                
            response = self.model.generate_content(system_prompt)
            
            # Clean up the response text to extract JSON
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            extracted_data = json.loads(response_text)
            
            # Update the current memory with extracted data
            updated_memory = current_memory.copy()
            for key, value in extracted_data.items():
                if hasattr(updated_memory, key) and value is not None:
                    setattr(updated_memory, key, value)
                    
            return updated_memory
            
        except Exception as e:
            print(f"Error in information extraction: {e}")
            return current_memory
    
    def generate_response(self, user_message: str, memory: SlotMemory, products: List[Dict] = None) -> str:
        """Generate natural conversational response"""
        
        # Calculate completion percentage
        filled_slots = 0
        total_important_slots = 6  # budget, purpose, ram, storage, properties, performance_needs
        
        if memory.budget is not None: filled_slots += 1
        if memory.purpose is not None: filled_slots += 1
        if memory.ram is not None: filled_slots += 1
        if memory.storage is not None: filled_slots += 1
        if len(memory.properties) > 0: filled_slots += 1
        if memory.performance_needs is not None: filled_slots += 1
        
        completion_percentage = filled_slots / total_important_slots
        
        if products:  # We have products to recommend
            system_prompt = f"""
You are a friendly and knowledgeable product recommendation assistant. 
The user has provided enough information and here are the recommended products based on their preferences:

User preferences: {memory.dict()}
Recommended products: {products}

Generate a natural, conversational response that:
1. Acknowledges their preferences
2. Presents the recommended products in a friendly way
3. Highlights why each product matches their needs
4. Asks if they need more information about any product

Keep the response conversational and helpful, not robotic.

User message: "{user_message}"
"""
        else:  # Need more information
            system_prompt = f"""
You are a friendly and knowledgeable product recommendation assistant.
The user is looking for product recommendations but you need more information.

Current information gathered: {memory.dict()}
Completion: {completion_percentage:.0%}

Generate a natural, conversational response that:
1. Acknowledges what they've told you so far
2. Asks for one or two specific pieces of missing information
3. Explains why this information is helpful
4. Keeps the conversation flowing naturally

Missing important information to ask about:
- Budget (if not provided)
- Purpose/use case (if not provided)  
- Performance needs (if not provided)
- RAM requirements (if not provided)
- Storage needs (if not provided)
- Any specific properties they care about (if not provided)

Be friendly and conversational, not like a form to fill out.

User message: "{user_message}"
"""
        
        try:
            if not self.model:
                # Fallback response if no API key
                print("No LLM model available, using fallback response")
                if completion_percentage >= 0.8:
                    return "I have enough information to find some great options for you! Let me search for products that match your needs."
                else:
                    return "Thanks for that information! Could you tell me a bit more about your budget and what you'll primarily use the device for?"
            
            print(f"Sending request to Google Gemini API with prompt length: {len(system_prompt)}")
            response = self.model.generate_content(system_prompt)
            print(f"Successfully received response from Google Gemini API")
            return response.text.strip()
            
        except Exception as e:
            print(f"Error generating response from Gemini API: {str(e)}")
            print(f"Trace: {e.__traceback__}")
            if completion_percentage >= 0.8:
                return "I have enough information to find some great options for you! Let me search for products that match your needs."
            else:
                return "Thanks for that information! Could you tell me a bit more about your budget and what you'll primarily use the device for?"

llm_service = LLMService()
