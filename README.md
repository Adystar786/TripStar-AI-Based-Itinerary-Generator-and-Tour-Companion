# TripStar AI - Smart Itinerary Generator

A powerful Flask-based web application that uses Google's Gemini AI to generate personalized travel itineraries.

## 🚀 Features

- **AI-Powered Itineraries**: Uses Gemini AI to create detailed, personalized travel plans
- **Multiple Destinations**: Support for adding multiple countries to your trip
- **Complete Currency Support**: 40+ international currencies
- **Dynamic Interests**: AI adapts suggestions based on destination and preferences
- **Beautiful PDF Export**: Professional, formatted PDF downloads
- **WhatsApp Sharing**: Easy sharing via WhatsApp
- **Trending Spots**: Shows current popular locations in your destinations
- **Responsive Design**: Works perfectly on all devices

## 📁 Project Structure

```
tripstar-ai/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
└── templates/
    └── index.html        # Main HTML template
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A Google Gemini API key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step 1: Clone or Download the Project

```bash
mkdir tripstar-ai
cd tripstar-ai
```

### Step 2: Create Project Files

Create the following structure:
- `app.py` (copy the Python code)
- `requirements.txt` (copy the requirements)
- `templates/index.html` (copy the HTML template)

### Step 3: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure Your Gemini API Key

Open `app.py` and replace the placeholder with your actual API key:

```python
# Line 10 in app.py
GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

**🔒 Security Best Practice**: For production, use environment variables:

1. Create a `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

2. Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

3. Add `.env` to `.gitignore`:
```
.env
venv/
__pycache__/
*.pyc
```

### Step 6: Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## 🎯 How to Use

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Fill in the form**:
   - Enter your name
   - Select destination(s) - can add multiple countries
   - Choose travel dates (start and end date)
   - Select traveler type (Solo, Couple, Family, Group)
   - Optionally select interests
   - Choose your currency
   - Enter your budget amount
   - Add any special notes (optional)
3. **Click "Generate AI Itinerary"**
4. **Wait** for the AI to create your personalized itinerary (usually 10-30 seconds)
5. **View your itinerary** with:
   - Day-by-day detailed plans
   - Specific activities and timings
   - Pro tips for each day
   - Currently trending spots in your destinations
   - Complete trip summary
6. **Download PDF** or **Share via WhatsApp**

## 🔐 Security Recommendations

### For Development:
- Store API key in `.env` file (never commit to Git)
- Add `.env` to `.gitignore`

### For Production:
- Use environment variables on your hosting platform
- Consider implementing user authentication
- Add rate limiting to prevent API abuse
- Use HTTPS for all connections

## 🌐 Deployment Options

### Option 1: Deploy to Heroku

1. Create a `Procfile`:
```
web: gunicorn app:app
```

2. Add `gunicorn` to requirements.txt:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

3. Deploy:
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

### Option 2: Deploy to Render

1. Connect your GitHub repository
2. Set environment variable: `GEMINI_API_KEY`
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`

### Option 3: Deploy to PythonAnywhere

1. Upload your files
2. Create a new web app (Flask)
3. Set up virtual environment
4. Configure WSGI file
5. Add API key to environment variables

### Option 4: Deploy to Railway

1. Connect GitHub repository
2. Add environment variable: `GEMINI_API_KEY`
3. Railway auto-detects Flask and deploys

## 🎨 Customization

### Modify Countries List
Edit the `COUNTRIES` list in `app.py` (line 15)

### Modify Currencies
Edit the `CURRENCIES` list in `app.py` (line 40)

### Change AI Model
Replace `'gemini-pro'` with other Gemini models in `app.py` (line 13)

### Customize Styling
Edit the CSS in `templates/index.html` (inside `<style>` tags)

### Modify Pricing Plans
Edit the pricing section in `templates/index.html` (search for "pricing-section")

## 📝 API Usage Notes

### Gemini API Limits
- **Free Tier**: 60 requests per minute
- Each itinerary generation = 1 API request
- Monitor your usage at [Google AI Studio](https://makersuite.google.com/)

### Response Time
- Typical generation time: 10-30 seconds
- Depends on itinerary complexity and API load

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "API Key Error"
- Verify your Gemini API key is correct
- Check if API key has proper permissions
- Ensure you haven't exceeded API quota

### "Template Not Found"
- Ensure `index.html` is in the `templates/` folder
- Check folder structure matches requirements

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### JSON Parse Error
- This usually means the AI response format changed
- Check the console logs for the actual response
- The app includes error handling for this

## 🔧 Advanced Configuration

### Enable Debug Mode
Already enabled by default in `app.py`:
```python
app.run(debug=True, port=5000)
```

**Important**: Disable debug mode in production:
```python
app.run(debug=False, port=5000)
```

### Add Rate Limiting
Install Flask-Limiter:
```bash
pip install Flask-Limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

@app.route('/generate-itinerary', methods=['POST'])
@limiter.limit("5 per hour")
def generate_itinerary():
    # ... existing code
```

### Add Database Support
For storing itineraries, add SQLAlchemy:
```bash
pip install Flask-SQLAlchemy
```

## 📊 Features Roadmap

- [ ] User authentication and accounts
- [ ] Save/favorite itineraries
- [ ] Email PDF export
- [ ] Multi-language support
- [ ] Weather integration
- [ ] Flight and hotel suggestions
- [ ] Budget breakdown by category
- [ ] Interactive map integration
- [ ] Social sharing (Twitter, Facebook)
- [ ] Collaborative trip planning

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips for Best Results

1. **Be Specific**: The more details you provide, the better the itinerary
2. **Reasonable Budget**: Enter realistic budgets for accurate recommendations
3. **Multiple Destinations**: Works great for multi-city trips
4. **Special Notes**: Use this field for dietary restrictions, accessibility needs, etc.
5. **Interests**: Selecting interests helps AI tailor activities to your preferences

## 🆘 Support

For issues or questions:
- Check the Troubleshooting section above
- Review [Flask documentation](https://flask.palletsprojects.com/)
- Check [Gemini AI documentation](https://ai.google.dev/docs)
- Open an issue on GitHub (if applicable)

## 🎉 Enjoy Your Trip Planning!

Happy travels! 🌍✈️🎒