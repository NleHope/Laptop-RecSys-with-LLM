# AI-Powered Chatbot for Product Recommendations

This is a full-stack AI-powered chatbot system designed for e-commerce stores to recommend products (specifically laptops) based on customer preferences using slot-filling memory management.

## 🚀 Features

- **Smart Conversation Flow**: Uses slot-filling to gradually collect customer preferences
- **LLM Integration**: Leverages OpenAI API for natural language understanding and response generation
- **Product Database**: SQLite database with comprehensive laptop catalog
- **Popup Chat Widget**: Responsive chat interface that integrates into any website
- **Real-time Recommendations**: Queries database and provides personalized product suggestions

## 🏗️ Architecture

### Backend (FastAPI)
- **Memory Management**: Slot-filling system tracks customer preferences
- **LLM Service**: Extracts structured data from natural language input
- **Product Search**: Dynamic database queries based on filled slots
- **Session Management**: Maintains conversation context per user

### Frontend (Vanilla JS)
- **Chat Widget**: Responsive popup interface
- **Real-time Communication**: REST API integration
- **Product Display**: Interactive product recommendations
- **Session Persistence**: Maintains conversation across page refreshes

### Database (SQLite)
- **Products Table**: Comprehensive laptop specifications
- **Chat Sessions**: User conversation history and memory state

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Edit .env file
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./chatbot.db
```

4. Initialize the database:
```bash
python init_db.py
```

5. Start the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `index.html` in a web browser or serve with a simple HTTP server:
```bash
# Option 1: Direct file access
open index.html

# Option 2: Python HTTP server
python -m http.server 3000
```

## 📋 API Endpoints

### Chat Endpoints
- `POST /chat` - Main chat endpoint
- `POST /session/new` - Create new chat session
- `GET /session/{session_id}/memory` - Get session memory (debug)

### Product Endpoints
- `GET /products/search` - Direct product search with filters

## 🧠 Slot-Filling Memory Structure

```json
{
  "budget": 1000.0,
  "ram": 16,
  "storage": 512,
  "purpose": "education",
  "properties": ["thin", "light"],
  "upgradability": "ram",
  "category": "laptop",
  "brand_preference": "Dell",
  "screen_size": "medium",
  "weight_preference": "light",
  "performance_needs": "medium"
}
```

## 🎯 Example Conversation Flow

**User**: "I need a laptop for college under $800"

**System Extracts**: `{budget: 800, purpose: "education"}`

**Bot**: "Great! A laptop for college under $800. Do you have any preferences for RAM or storage? Also, do you need something portable for carrying around campus?"

**User**: "Yes, something light with good RAM for multitasking"

**System Extracts**: `{weight_preference: "light", ram: 16, performance_needs: "medium"}`

**Bot**: "Perfect! Here are some great lightweight laptops under $800 with good RAM for college..."

## 🔧 Customization

### Adding New Product Categories
1. Update the `Product` model in `database.py`
2. Modify the `SlotMemory` model in `models.py`
3. Update the LLM prompts in `llm_service.py`
4. Adjust the product search logic in `services.py`

### Modifying the Chat Interface
- Edit `chatbot.css` for styling changes
- Modify `chatbot.js` for functionality updates
- Update `index.html` for layout changes

### Changing LLM Provider
Update the `LLMService` class in `llm_service.py` to use different providers (Anthropic, local models, etc.)

## 📱 Integration

To integrate the chat widget into your existing website:

1. Include the CSS and JS files:
```html
<link rel="stylesheet" href="path/to/chatbot.css">
<script src="path/to/chatbot.js"></script>
```

2. Add the chat widget HTML:
```html
<!-- Copy the chat widget elements from index.html -->
```

3. Update the API URL in `chatbot.js`:
```javascript
this.apiUrl = 'https://your-backend-domain.com';
```

## 🚦 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM integration | Required |
| `DATABASE_URL` | Database connection string | `sqlite:///./chatbot.db` |

## 🧪 Testing

### Backend Testing
```bash
# Test the API directly
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a gaming laptop", "session_id": "test-session"}'
```

### Frontend Testing
Open the frontend in a browser and test the conversation flow with various queries:
- Budget constraints
- Specific use cases (gaming, education, business)
- Technical requirements (RAM, storage, weight)
- Brand preferences

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the browser console for frontend errors
3. Check the backend logs for API issues

## 🔮 Future Enhancements

- [ ] Support for multiple product categories
- [ ] Advanced filtering and sorting options
- [ ] Integration with payment systems
- [ ] Multi-language support
- [ ] Analytics and conversation insights
- [ ] Voice input support
- [ ] Mobile app version
