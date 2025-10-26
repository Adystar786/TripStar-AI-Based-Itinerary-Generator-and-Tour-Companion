from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import os
from datetime import datetime, timedelta
import logging
import uuid
from models import db, User, Itinerary, UsageRecord, Payment  # ✅ Single import - Payment is in models.py
import qrcode
from io import BytesIO
import base64
import re
from dotenv import load_dotenv

load_dotenv()

# Country interests mapping for AI suggestions
countryInterests = {
    "France": ["Wine Tasting", "Art Museums", "Historical Sites", "Gourmet Food", "Shopping", "Romantic Getaways", "Eiffel Tower", "Louvre Museum", "French Riviera", "Provence Lavender Fields", "Normandy D-Day Beaches", "Loire Valley Castles"],
    "Italy": ["Historical Sites", "Art Museums", "Wine Tasting", "Cooking Classes", "Beach Relaxation", "Shopping", "Colosseum", "Venice Canals", "Tuscany Countryside", "Vatican City", "Amalfi Coast", "Italian Lakes"],
    "Japan": ["Temples & Shrines", "Anime & Manga", "Sushi Making", "Hot Springs", "Cherry Blossoms", "Shopping", "Mount Fuji", "Tokyo Nightlife", "Traditional Gardens", "Bullet Train Experience", "Kyoto Geisha Districts", "Osaka Street Food"],
    "USA": ["National Parks", "Theme Parks", "Shopping", "Beach Activities", "City Tours", "Food Tours", "Route 66 Road Trip", "New York Broadway", "Las Vegas Entertainment", "Grand Canyon", "California Coast", "Historical Landmarks"],
    "Spain": ["Flamenco Shows", "Beach Relaxation", "Historical Sites", "Tapas Tours", "Shopping", "Nightlife", "Sagrada Familia", "Alhambra Palace", "Ibiza Clubs", "Madrid Art Museums", "Barcelona Architecture", "Andalusian Culture"],
    "Thailand": ["Temples", "Beach Activities", "Elephant Sanctuaries", "Street Food", "Island Hopping", "Shopping", "Buddhist Temples", "Thai Massage", "Floating Markets", "Full Moon Parties", "Jungle Trekking", "Muay Thai"],
    "India": ["Historical Monuments", "Yoga & Meditation", "Spiritual Sites", "Local Markets", "Wildlife Safaris", "Food Tours", "Taj Mahal", "Himalayan Trekking", "Kerala Backwaters", "Rajasthan Palaces", "Varanasi Ghats", "Goa Beaches"],
    "Australia": ["Beach Activities", "Wildlife Viewing", "Wine Tasting", "Outdoor Adventures", "City Tours", "Great Barrier Reef", "Sydney Opera House", "Outback Exploration", "Surfing Lessons", "Koala Sanctuaries", "Gold Coast Theme Parks", "Indigenous Culture"],
    "Greece": ["Historical Sites", "Island Hopping", "Beach Relaxation", "Greek Cuisine", "Sunset Views", "Shopping", "Acropolis", "Santorini Sunsets", "Mykonos Nightlife", "Ancient Ruins", "Mediterranean Cooking", "Olive Oil Tasting"],
    "Germany": ["Historical Sites", "Beer Tasting", "Castle Tours", "Christmas Markets", "City Tours", "Museums", "Neuschwanstein Castle", "Berlin Wall", "Oktoberfest", "Black Forest", "Romantic Road", "River Cruises"],
    "default": ["Historical Sites", "Local Cuisine", "Shopping", "Nature & Parks", "Cultural Experiences", "Adventure Activities", "Photography", "Wellness & Spas", "Nightlife", "Family Activities", "Art & Museums", "Beach Relaxation"]
}

# Import your AI models with proper error handling
AI_AVAILABLE = False
ai_model = None

try:
    from model_config import TripStarAIModel
    AI_AVAILABLE = True
    print("✅ AI models imported successfully")
except ImportError as e:
    print(f"❌ AI models not available: {e}")
    AI_AVAILABLE = False
except Exception as e:
    print(f"❌ Error importing AI models: {e}")
    AI_AVAILABLE = False

# Initialize AI model safely
if AI_AVAILABLE:
    try:
        ai_model = TripStarAIModel()
        if ai_model and hasattr(ai_model, 'client') and ai_model.client:
            print("✅ AI model initialized successfully")
        else:
            print("❌ AI model initialized but client not available")
            ai_model = None
    except Exception as e:
        print(f"❌ AI model initialization failed: {e}")
        ai_model = None
else:
    ai_model = None
    print("⚠️ Running without AI capabilities")

app = Flask(__name__)

# CRITICAL: Configure database URL from environment
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Fix for Heroku/Render postgres:// -> postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tripstar-ai-secret-key-2025-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 5,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'connect_args': {
        'sslmode': 'require'
    }
}

# Initialize extensions
db.init_app(app)
CORS(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'welcome'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/')
def welcome():
    """Welcome page - similar to Viator"""
    return render_template('welcome.html')

@app.route('/home')
@login_required
def home():
    """Redirect to dashboard from home if authenticated"""
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard after login"""
    free_uses_remaining = current_user.get_remaining_free_uses()
    return render_template('index.html', 
                         user=current_user,
                         free_uses_remaining=free_uses_remaining)

@app.route('/auth/register', methods=['POST'])
def register():
    """Handle user registration"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        
        # Validate input
        if not all([email, password, first_name, last_name]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            plan='free'  # Default plan
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Log the user in
        login_user(user)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'plan': user.plan
            }
        })
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Registration failed'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'plan': user.plan
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500

@app.route('/auth/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    return redirect(url_for('welcome'))

@app.route('/auth/check')
def check_auth():
    """Check if user is authenticated"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                'plan': current_user.plan
            }
        })
    else:
        return jsonify({'authenticated': False})

@app.route('/auth/clear-session')
def clear_session():
    """Clear all session data - for testing purposes"""
    from flask import session
    session.clear()
    logout_user()
    return jsonify({'success': True, 'message': 'Session cleared'})

@app.route('/auth/force-logout')
def force_logout():
    """Force logout and clear all session data"""
    logout_user()
    from flask import session
    session.clear()
    return redirect(url_for('welcome'))

# ============================================================================
# PLAN & USAGE ROUTES
# ============================================================================

@app.route('/update-plan', methods=['POST'])
@login_required
def update_plan():
    """Update user's plan"""
    try:
        data = request.get_json()
        plan = data.get('plan')
        
        if plan not in ['free', 'pro', 'per_export']:
            return jsonify({'success': False, 'error': 'Invalid plan'}), 400
        
        current_user.plan = plan
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Plan updated to {plan}',
            'plan': plan
        })
        
    except Exception as e:
        logger.error(f"Plan update error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Plan update failed'}), 500

@app.route('/get-usage')
@login_required
def get_usage():
    """Get current usage data for the user"""
    free_uses_remaining = current_user.get_remaining_free_uses()
    
    return jsonify({
        'free_uses_remaining': free_uses_remaining,
        'plan': current_user.plan,
        'last_reset': datetime.utcnow().date().isoformat()
    })

@app.route('/check-pro-access')
@login_required
def check_pro_access():
    """Check if user has pro access"""
    free_uses_remaining = current_user.get_remaining_free_uses()
    return jsonify({
        'is_pro': current_user.plan == 'pro',
        'plan': current_user.plan,
        'unlimited_access': current_user.plan == 'pro',
        'free_uses_remaining': free_uses_remaining
    })

# ============================================================================
# ITINERARY GENERATION ROUTES
# ============================================================================

@app.route('/generate-itinerary', methods=['POST'])
@login_required
def generate_itinerary():
    """Generate AI-powered itinerary"""
    try:
        data = request.get_json()
        
        logger.info(f"Generating itinerary for user: {current_user.email}")
        logger.info(f"User plan: {current_user.plan}")
        
        # Check free plan usage
        if current_user.plan == 'free':
            free_uses_remaining = current_user.get_remaining_free_uses()
            if free_uses_remaining <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Daily free limit reached. Upgrade to Pro for unlimited itineraries.'
                }), 429
            
            # Record usage
            usage = UsageRecord(
                user_id=current_user.id, 
                plan='free', 
                action='itinerary_generation'
            )
            db.session.add(usage)
        
        # Validate required fields
        required_fields = ['userName', 'destinations', 'startDate', 'endDate', 'travelerType', 'budget']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Prepare AI input data
        ai_input_data = {
            'user_name': data['userName'],
            'destinations': data['destinations'],
            'destination_codes': data.get('destinationCodes', []),
            'start_date': data['startDate'],
            'end_date': data['endDate'],
            'traveler_type': data['travelerType'],
            'budget': float(data['budget']),
            'currency_symbol': data.get('currencySymbol', '$'),
            'interests': data.get('interests', ''),
            'notes': data.get('notes', ''),
            'plan': current_user.plan,
            'budget_friendly': data.get('budgetFriendly', False),
            'departure_city': data.get('departureCity', ''),
            'departure_city_code': data.get('departureCityCode', '')
        }
        
        # Calculate days
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        ai_input_data['days'] = (end_date - start_date).days + 1
        
        print(f"🎯 Generating {ai_input_data['days']}-day itinerary...")
        
        # Generate itinerary
        if AI_AVAILABLE and ai_model and ai_model.client:
            itinerary = ai_model.generate_itinerary(ai_input_data)
        else:
            itinerary = generate_fallback_itinerary(ai_input_data)
        
        if itinerary:
            # Save to database
            new_itinerary = Itinerary(
                user_id=current_user.id,
                title=f"{', '.join(data['destinations'])} Itinerary",
                destinations=json.dumps(data['destinations']),
                travel_dates=json.dumps({
                    'start_date': data['startDate'],
                    'end_date': data['endDate']
                }),
                traveler_type=data['travelerType'],
                budget=float(data['budget']),
                currency=data.get('currencySymbol', '$'),
                interests=data.get('interests', ''),
                notes=data.get('notes', ''),
                plan_used=current_user.plan
            )
            new_itinerary.set_itinerary_data(itinerary)
            
            db.session.add(new_itinerary)
            db.session.commit()
            
            logger.info(f"Itinerary generated and saved for {current_user.email}")
            
            free_uses_remaining = current_user.get_remaining_free_uses()
            return jsonify({
                'success': True,
                'itinerary': itinerary,
                'free_uses_remaining': free_uses_remaining,
                'itinerary_id': new_itinerary.id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate itinerary'
            }), 500
        
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

def generate_fallback_itinerary(data):
    """Generate fallback itinerary when AI fails"""
    days = data['days']
    destinations = data['destinations']
    traveler_type = data['traveler_type']
    budget = data['budget']
    currency_symbol = data['currency_symbol']
    
    destination_name = destinations[0] if destinations else "your destination"
    
    itinerary = {
        "days": [],
        "popularSpots": [
            {
                "name": f"{destination_name} Historic Center",
                "description": f"Explore the cultural heart of {destination_name} with stunning architecture."
            },
            {
                "name": "Local Food Markets", 
                "description": f"Experience authentic culinary traditions at {destination_name}'s markets."
            }
        ],
        "summary": f"This {days}-day journey through {destination_name} is designed for {traveler_type.lower()} travelers."
    }
    
    for day in range(1, days + 1):
        itinerary["days"].append({
            "day": day,
            "title": f"Day {day} in {destination_name}",
            "description": f"Explore {destination_name}'s attractions.",
            "activities": [
                "Morning: Cultural site visits",
                "Afternoon: Local experiences",
                "Evening: Dining and relaxation"
            ],
            "tip": "Wear comfortable shoes and stay hydrated."
        })
    
    return itinerary

# ============================================================================
# AI INTERESTS ROUTE
# ============================================================================

@app.route('/get-ai-interests', methods=['POST'])
@login_required
def get_ai_interests():
    """Get AI-suggested interests based on destinations"""
    try:
        data = request.get_json()
        destinations = data.get('destinations', [])
        
        if not destinations:
            return jsonify({'interests': []})
        
        if not AI_AVAILABLE or not ai_model or not ai_model.client:
            # Fallback to static interests
            all_interests = set()
            for destination in destinations:
                interests = countryInterests.get(destination, countryInterests['default'])
                all_interests.update(interests)
            
            interests_with_emojis = add_emojis_to_interests(list(all_interests)[:15])
            return jsonify({'interests': interests_with_emojis})
        
        # Use AI to generate relevant interests
        destinations_str = ', '.join(destinations)
        prompt = f"""Based on these travel destinations: {destinations_str}
        
        Suggest 15 most relevant travel interest categories.
        Return ONLY a JSON array of strings, no explanations, no emojis.
        
        Example: ["Historical Sites", "Local Cuisine", "Adventure Sports"]"""
        
        response = ai_model.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a travel expert. Respond with ONLY a JSON array of strings."},
                {"role": "user", "content": prompt}
            ],
            model=ai_model.model_name,
            temperature=0.7,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        try:
            interests = json.loads(response_text)
            if isinstance(interests, list):
                interests_with_emojis = add_emojis_to_interests(interests)
                return jsonify({'interests': interests_with_emojis})
        except json.JSONDecodeError:
            pass
        
        # Fallback
        all_interests = set()
        for destination in destinations:
            interests = countryInterests.get(destination, countryInterests['default'])
            all_interests.update(interests)
        
        interests_with_emojis = add_emojis_to_interests(list(all_interests)[:15])
        return jsonify({'interests': interests_with_emojis})
        
    except Exception as e:
        logger.error(f"Error getting AI interests: {str(e)}")
        all_interests = set()
        for destination in destinations:
            interests = countryInterests.get(destination, countryInterests['default'])
            all_interests.update(interests)
        
        interests_with_emojis = add_emojis_to_interests(list(all_interests)[:15])
        return jsonify({'interests': interests_with_emojis})

def add_emojis_to_interests(interests):
    """Add relevant emojis to interest categories"""
    emoji_map = {
        'historical': '🏛️', 'food': '🍽️', 'beach': '🏖️', 'art': '🎨',
        'shopping': '🛍️', 'nature': '🌿', 'adventure': '🏔️', 'water': '🌊',
        'wildlife': '🦁', 'culture': '🎭', 'nightlife': '🌃', 'wellness': '🧘',
        'photo': '📸', 'wine': '🍷', 'temple': '🛕', 'family': '👨‍👩‍👧‍👦'
    }
    
    interests_with_emojis = []
    for interest in interests:
        emoji = '🎯'
        for keyword, mapped_emoji in emoji_map.items():
            if keyword in interest.lower():
                emoji = mapped_emoji
                break
        interests_with_emojis.append(f"{interest} {emoji}")
    
    return interests_with_emojis

# ============================================================================
# FLIGHT SEARCH ROUTES
# ============================================================================

@app.route('/search-flights', methods=['POST'])
@login_required
def search_flights():
    """Search for best flights"""
    try:
        data = request.get_json()
        departure_city = data.get('departure_city', '')
        departure_city_code = data.get('departure_city_code', '')
        destinations = data.get('destinations', [])
        destination_codes = data.get('destination_codes', [])
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        budget = data.get('budget', 1000)
        currency_symbol = data.get('currency_symbol', '$')
        
        if not departure_city or not destinations or not start_date or not end_date:
            return jsonify({
                'success': False, 
                'error': 'Missing required parameters'
            }), 400
        
        logger.info(f"Flight search: {departure_city} → {', '.join(destinations)}")
        
        flight_results = generate_fallback_flights(
            departure_city, departure_city_code, destinations, destination_codes,
            start_date, end_date, budget, currency_symbol
        )
        
        return jsonify({
            'success': True,
            'flights': flight_results
        })
        
    except Exception as e:
        logger.error(f"Flight search error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'Flight search failed'
        }), 500

def generate_fallback_flights(departure_city, departure_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol):
    """Generate fallback flight recommendations"""
    if not destinations or len(destinations) == 0:
        return {"flights": [], "searchLink": "#", "generalTips": ["Please select destinations"]}
    
    flights = []
    destination = destinations[0]
    
    flights.append({
        "routeType": "round-trip",
        "destination": destination,
        "departureCity": departure_city,
        "outboundDate": start_date,
        "returnDate": end_date,
        "options": [
            {
                "airline": "Major Airlines",
                "flightNumber": "Multiple options available",
                "cabinClasses": {
                    "economy": {
                        "price": f"{currency_symbol}{int(budget * 0.3)}",
                        "available": True
                    }
                },
                "duration": "Varies",
                "stops": "0-2",
                "bookingLink": f"https://www.google.com/travel/flights",
                "moneySavingTips": [
                    "Book 6-8 weeks in advance",
                    "Consider nearby airports"
                ]
            }
        ]
    })
    
    return {
        "flights": flights,
        "searchLink": "https://www.google.com/travel/flights",
        "generalTips": [
            "Book flights 6-8 weeks in advance",
            "Be flexible with dates",
            "Check baggage policies"
        ]
    }

# ============================================================================
# PAYMENT ROUTES (FIXED - NO payment_models imports)
# ============================================================================

@app.route('/payment')
@login_required
def payment_page():
    """Payment page for upgrading to pro"""
    return render_template('payment.html')

@app.route('/payment/generate-qr', methods=['POST'])
@login_required
def generate_qr():
    """Generate UPI QR code for payment"""
    try:
        data = request.get_json()
        plan = data.get('plan', 'pro')
        
        amount = 499 if plan == 'pro' else 99
        upi_id = "adnanstar786-1@oksbi"
        merchant_name = "TripStarAI"
        
        payment_id = str(uuid.uuid4())[:8]
        upi_string = f"upi://pay?pa={upi_id}&pn={merchant_name}&am={amount}&cu=INR&tn=TripStarPro-{payment_id}"
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(upi_string)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # ✅ Payment is already imported from models at the top
        payment = Payment(
            user_id=current_user.id,
            payment_id=payment_id,
            plan=plan,
            amount=amount,
            status='pending',
            upi_id=upi_id
        )
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'qr_code': f"data:image/png;base64,{img_str}",
            'payment_id': payment_id,
            'upi_id': upi_id,
            'amount': amount,
            'upi_string': upi_string
        })
        
    except Exception as e:
        logger.error(f"QR generation error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/payment/initiate', methods=['POST'])
@login_required
def initiate_payment():
    """Initiate payment for pro plan"""
    try:
        data = request.get_json()
        plan = data.get('plan', 'pro')
        
        if plan not in ['pro', 'per_export']:
            return jsonify({'success': False, 'error': 'Invalid plan'}), 400
        
        payment_id = str(uuid.uuid4())
        amount = 499 if plan == 'pro' else 99
        
        # ✅ Payment is already imported from models
        payment = Payment(
            user_id=current_user.id,
            payment_id=payment_id,
            plan=plan,
            amount=amount,
            status='initiated'
        )
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'payment_id': payment_id,
            'amount': amount,
            'plan': plan,
            'upi_id': 'adnanstar786-1@oksbi',
            'contact_email': 'adystar67@gmail.com'
        })
        
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Payment initiation failed'}), 500

@app.route('/payment/verify', methods=['POST'])
@login_required
def verify_payment():
    """Verify payment"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        transaction_id = data.get('transaction_id')
        
        if not transaction_id:
            return jsonify({'success': False, 'error': 'Transaction ID is required'}), 400
        
        # ✅ Payment is already imported
        payment = Payment.query.filter_by(payment_id=payment_id, user_id=current_user.id).first()
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment record not found'}), 404
        
        payment.transaction_id = transaction_id
        payment.status = 'pending_verification'
        db.session.commit()
        
        logger.info(f"Payment verification pending - User: {current_user.email}, Transaction: {transaction_id}")
        
        return jsonify({
            'success': True,
            'message': 'Payment submitted for verification. You will be upgraded within 2-4 hours.',
            'pending': True
        })
        
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Payment verification failed'}), 500
        
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Payment verification failed'}), 500

@app.route('/payment/manual-verification', methods=['POST'])
@login_required
def manual_verification():
    """Manual payment verification"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        user_upi_id = data.get('upi_id')
        amount = data.get('amount')
        
        if not user_upi_id:
            return jsonify({'success': False, 'error': 'UPI ID is required'}), 400
        
        # ✅ Payment is already imported
        payment = Payment.query.filter_by(payment_id=payment_id, user_id=current_user.id).first()
        
        if payment:
            payment.upi_id = user_upi_id
            payment.status = 'manual_verification_pending'
            db.session.commit()
        
        logger.info(f"Manual verification requested - User: {current_user.email}, Payment: {payment_id}")
        
        return jsonify({
            'success': True,
            'message': 'Manual verification request submitted. We will verify within 24 hours.',
            'contact_email': 'adystar67@gmail.com',
            'pending': True
        })
        
    except Exception as e:
        logger.error(f"Manual verification error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Manual verification request failed'}), 500

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin/payments')
@login_required
def admin_payments():
    """Admin page to view and approve payments"""
    if current_user.email != 'adystar67@gmail.com':
        return redirect(url_for('dashboard'))
    
    # ✅ Payment is already imported
    pending_payments = Payment.query.filter(
        Payment.status.in_(['pending_verification', 'manual_verification_pending'])
    ).order_by(Payment.created_at.desc()).all()
    
    return render_template('admin_payments.html', payments=pending_payments)

@app.route('/admin/approve-payment/<int:payment_id>', methods=['POST'])
@login_required
def approve_payment(payment_id):
    """Admin approves a payment"""
    if current_user.email != 'adystar67@gmail.com':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        # ✅ Payment is already imported
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        # Upgrade user to pro
        user = User.query.get(payment.user_id)
        user.plan = 'pro'
        
        # Update payment status
        payment.status = 'completed'
        payment.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Payment approved by admin - User: {user.email}, Payment: {payment.payment_id}")
        
        return jsonify({'success': True, 'message': 'Payment approved and user upgraded'})
        
    except Exception as e:
        logger.error(f"Payment approval error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/reject-payment/<int:payment_id>', methods=['POST'])
@login_required
def reject_payment(payment_id):
    """Admin rejects a payment"""
    if current_user.email != 'adystar67@gmail.com':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        # ✅ Payment is already imported
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        data = request.get_json()
        reason = data.get('reason', 'Payment verification failed')
        
        payment.status = 'rejected'
        db.session.commit()
        
        user = User.query.get(payment.user_id)
        logger.info(f"Payment rejected by admin - User: {user.email}, Reason: {reason}")
        
        return jsonify({'success': True, 'message': 'Payment rejected'})
        
    except Exception as e:
        logger.error(f"Payment rejection error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# UTILITY ROUTES
# ============================================================================

@app.route('/test-ai')
def test_ai():
    """Test route to verify AI model is working"""
    if not AI_AVAILABLE or not ai_model or not ai_model.client:
        return jsonify({'status': 'AI not available'})
    
    try:
        test_data = {
            'user_name': 'Test User',
            'destinations': ['France'],
            'start_date': '2025-01-01',
            'end_date': '2025-01-03',
            'traveler_type': 'Solo',
            'budget': 2000,
            'currency_symbol': '$',  # ✅ FIXED: Added missing quote and value
            'interests': 'Historical Sites, Food',
            'notes': 'Test itinerary',
            'plan': 'free',
            'days': 3
        }
        
        result = ai_model.generate_itinerary(test_data)
        return jsonify({
            'status': 'AI working',
            'test_result': 'Success' if result else 'Failed',
            'days_generated': len(result.get('days', [])) if result else 0
        })
        
    except Exception as e:
        return jsonify({'status': 'AI error', 'error': str(e)})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('static', filename)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """Initialize database tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify connection
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection verified!")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Available tables: {', '.join(tables)}")
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            import traceback
            traceback.print_exc()

# Initialize database on startup
print("🔧 Initializing database...")
init_database()

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting TripStar AI on port {port}...")
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI'][:30]}...")
    app.run(host="0.0.0.0", port=port, debug=True)
