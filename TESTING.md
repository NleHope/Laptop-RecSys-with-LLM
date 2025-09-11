# 🧪 Testing Guide for AI Chatbot System

This guide will help you test all the features of the AI-powered chatbot system.

## 🚀 Quick Start Testing

### 1. System Status Check
- ✅ Backend API: http://localhost:8000 
- ✅ API Documentation: http://localhost:8000/docs
- ✅ Frontend: file:///d:/Actual%20Personal%20File/BaterialVagi/Images/chatbot-system/frontend/index.html

### 2. Basic API Test
Open your browser and go to http://localhost:8000 - you should see:
```json
{"message": "AI Chatbot API is running"}
```

## 💬 Chat Widget Testing

### Frontend Interface
1. Open the frontend in your browser
2. Look for the chat bubble icon (💬) in the bottom-right corner
3. Click it to open the chat widget
4. You should see a welcome message from the AI assistant

### Sample Conversations to Test

#### Test 1: Budget Laptop for Education
```
User: "I need a laptop for college under $800"
Expected: Bot asks for more details about preferences
User: "Something light for carrying around campus"
Expected: Bot may ask about RAM, storage, or recommend products
```

#### Test 2: Gaming Laptop
```
User: "I'm looking for a gaming laptop with good graphics"
Expected: Bot asks about budget
User: "Around $1500"
Expected: Bot should recommend gaming laptops like ASUS ROG or HP Omen
```

#### Test 3: Business Laptop
```
User: "I need something for work, portable and reliable"
Expected: Bot asks for budget and specific requirements
User: "Budget is $1000, need good battery life"
Expected: Bot should recommend business laptops like ThinkPad
```

#### Test 4: Complete Specification
```
User: "I want a thin laptop under $1000 with 16GB RAM for programming"
Expected: Bot should quickly provide recommendations since many slots are filled
```

## 🔧 Backend API Testing

### Direct API Testing with curl (PowerShell)

#### 1. Test Chat Endpoint
```powershell
$body = @{
    message = "I need a gaming laptop under $1500"
    session_id = "test-session-123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

#### 2. Test Session Creation
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/session/new" -Method Post -ContentType "application/json"
```

#### 3. Test Product Search
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/products/search?budget=1000&category=laptop&purpose=gaming" -Method Get
```

#### 4. Check Session Memory
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/session/test-session-123/memory" -Method Get
```

## 🗄️ Database Testing

### Check Database Contents
```bash
# Navigate to backend directory
cd backend

# Open SQLite database
python -c "
import sqlite3
conn = sqlite3.connect('chatbot.db')
cursor = conn.cursor()

print('=== PRODUCTS TABLE ===')
cursor.execute('SELECT name, price, category, use_case FROM products LIMIT 5')
for row in cursor.fetchall():
    print(f'{row[0]} - \${row[1]} ({row[2]}) - {row[3]}')

print('\n=== CHAT SESSIONS TABLE ===')
cursor.execute('SELECT session_id, memory FROM chat_sessions LIMIT 3')
for row in cursor.fetchall():
    print(f'Session: {row[0][:20]}... Memory: {row[1][:50]}...')

conn.close()
"
```

## 🎯 Feature Testing Checklist

### ✅ Slot-Filling Memory System
- [ ] Budget extraction ("under $800", "$1000 budget")
- [ ] Purpose detection ("for gaming", "for school", "for work")
- [ ] Properties extraction ("thin", "light", "portable")
- [ ] RAM requirements ("16GB RAM", "good memory")
- [ ] Storage needs ("512GB storage", "large storage")
- [ ] Upgradability ("upgradable RAM")

### ✅ Product Recommendations
- [ ] Budget filtering works correctly
- [ ] Category filtering (laptops only)
- [ ] Use case matching (gaming, education, business)
- [ ] Technical specs filtering (RAM, storage)
- [ ] Weight/portability filtering
- [ ] Upgradability filtering

### ✅ Conversation Flow
- [ ] Asks clarifying questions when information is missing
- [ ] Provides recommendations when ~60% of slots are filled
- [ ] Maintains conversation context across messages
- [ ] Handles invalid/unclear input gracefully

### ✅ Frontend Features
- [ ] Chat widget opens/closes properly
- [ ] Messages display with correct styling
- [ ] Product cards show in recommendations
- [ ] Typing indicator appears during API calls
- [ ] Time stamps are accurate
- [ ] Responsive design on mobile

## 🐛 Troubleshooting

### Common Issues

#### "Import could not be resolved" errors
- These are just VS Code warnings, the code runs fine
- Packages are installed correctly in your Python environment

#### Chat widget not connecting
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify the API URL in chatbot.js

#### No product recommendations
- Check if database was seeded correctly
- Verify slot-filling is working (check session memory endpoint)
- Test with very specific requirements

#### OpenAI API errors
- The system automatically falls back to demo mode if API key is missing
- Set your API key in backend/.env if you want full LLM features

### Debug Commands

#### Check if backend is running
```powershell
Invoke-RestMethod -Uri "http://localhost:8000" -Method Get
```

#### View backend logs
Look at the terminal window where you started the backend server

#### Test database connection
```bash
python -c "from database import SessionLocal; db = SessionLocal(); print('Database connected successfully'); db.close()"
```

## 📊 Performance Testing

### Load Testing (Optional)
Use tools like Apache Bench or curl to test multiple concurrent requests:

```bash
# Test 100 requests with concurrency of 10
ab -n 100 -c 10 -H "Content-Type: application/json" -p test-payload.json http://localhost:8000/chat
```

### Memory Usage
Monitor Python process memory usage during extended chat sessions to ensure no memory leaks.

## 🎉 Success Indicators

Your system is working correctly if:
- ✅ Chat widget responds within 2-3 seconds
- ✅ Product recommendations are relevant to user input
- ✅ Conversation maintains context across messages
- ✅ Database queries return appropriate results
- ✅ No console errors in browser or backend
- ✅ Session memory persists across page refreshes

## 📝 Test Results Template

```
=== CHATBOT SYSTEM TEST RESULTS ===
Date: ___________
Tester: _________

Frontend Tests:
□ Chat widget opens/closes: PASS/FAIL
□ Message sending: PASS/FAIL
□ Product display: PASS/FAIL
□ Responsive design: PASS/FAIL

Backend Tests:
□ API connectivity: PASS/FAIL
□ Chat endpoint: PASS/FAIL
□ Product search: PASS/FAIL
□ Session management: PASS/FAIL

Slot-Filling Tests:
□ Budget extraction: PASS/FAIL
□ Purpose detection: PASS/FAIL
□ Properties extraction: PASS/FAIL
□ Technical specs: PASS/FAIL

Product Recommendations:
□ Accuracy: PASS/FAIL
□ Relevance: PASS/FAIL
□ Completeness: PASS/FAIL

Overall System: PASS/FAIL
Notes: ________________
```
