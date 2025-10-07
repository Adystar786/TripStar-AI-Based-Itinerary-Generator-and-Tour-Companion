from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import os
from datetime import datetime, timedelta
import logging
import uuid
from flask import request, jsonify, render_template
from models import db, User, Itinerary, UsageRecord

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

# Import your AI models
try:
    from model_config import TripStarAIModel
    from pro_model_config import TripStarProModel
    AI_AVAILABLE = True
    print("✅ AI models imported successfully")
except ImportError as e:
    print(f"❌ AI models not available: {e}")
    AI_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tripstar-ai-secret-key-2025-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tripstar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False

@app.route('/payment/initiate', methods=['POST'])
@login_required
def initiate_payment():
    """Initiate payment for pro plan"""
    try:
        data = request.get_json()
        plan = data.get('plan', 'pro')
        
        if plan not in ['pro', 'per_export']:
            return jsonify({'success': False, 'error': 'Invalid plan'}), 400
        
        # Create a unique payment ID
        payment_id = str(uuid.uuid4())
        
        # For pro plan - ₹499
        amount = 499 if plan == 'pro' else 99
        
        payment_data = {
            'payment_id': payment_id,
            'user_id': current_user.id,
            'plan': plan,
            'amount': amount,
            'status': 'initiated',
            'created_at': datetime.utcnow().isoformat()
        }
        
        # In a real implementation, you'd save this to a payments table
        # For now, we'll use session storage
        # You can create a Payment model later
        
        return jsonify({
            'success': True,
            'payment_id': payment_id,
            'amount': amount,
            'plan': plan,
            'upi_id': 'your-upi@okaxis',  # Replace with your actual UPI ID
            'contact_email': 'your-email@gmail.com'  # Replace with your email
        })
        
    except Exception as e:
        logger.error(f"Payment initiation error: {str(e)}")
        return jsonify({'success': False, 'error': 'Payment initiation failed'}), 500

@app.route('/payment/verify', methods=['POST'])
@login_required
def verify_payment():
    """Verify payment and upgrade user plan"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        transaction_id = data.get('transaction_id')
        
        # In a real implementation, you'd verify with your payment gateway
        # For now, we'll assume payment is successful if transaction_id is provided
        
        if not transaction_id:
            return jsonify({'success': False, 'error': 'Transaction ID is required'}), 400
        
        # Update user plan to pro
        current_user.plan = 'pro'
        db.session.commit()
        
        logger.info(f"User {current_user.email} upgraded to PRO plan. Transaction: {transaction_id}")
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully! Your account has been upgraded to PRO.',
            'plan': 'pro'
        })
        
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Payment verification failed'}), 500

@app.route('/payment/manual-verification', methods=['POST'])
@login_required
def manual_verification():
    """Manual payment verification for UPI payments"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        upi_id = data.get('upi_id')  # User's UPI ID for verification
        amount = data.get('amount')
        
        # Store manual verification request
        # In production, you'd save this to a database and notify admin
        logger.info(f"Manual verification requested - User: {current_user.email}, Payment ID: {payment_id}, Amount: {amount}, UPI: {upi_id}")
        
        # For now, auto-approve for testing (remove in production)
        # In production, you'd wait for admin verification
        current_user.plan = 'pro'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Manual verification request received. We will verify your payment and upgrade your account within 24 hours. For immediate activation, contact support.',
            'contact_email': 'your-email@gmail.com',  # Replace with your email
            'auto_approved': True  # Remove this in production
        })
        
    except Exception as e:
        logger.error(f"Manual verification error: {str(e)}")
        return jsonify({'success': False, 'error': 'Manual verification request failed'}), 500

# Update the generate_itinerary function to ensure pro users get unlimited access
# (The existing implementation should already handle this, but let's add a check)

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

# Initialize AI model
if AI_AVAILABLE:
    ai_model = TripStarAIModel()
else:
    ai_model = None
    print("⚠️ Running without AI capabilities")

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def welcome():
    """Welcome page - similar to Viator"""
    # Always show welcome page, even if user is authenticated
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
            usage = UsageRecord(user_id=current_user.id, plan='free', action='itinerary_generation')
            db.session.add(usage)
        
        # Validate required fields
        required_fields = ['userName', 'destinations', 'startDate', 'endDate', 'travelerType', 'budget']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Prepare data for AI model
        ai_input_data = {
            'user_name': data['userName'],
            'destinations': data['destinations'],
            'start_date': data['startDate'],
            'end_date': data['endDate'],
            'traveler_type': data['travelerType'],
            'budget': float(data['budget']),
            'currency_symbol': data.get('currencySymbol', '$'),
            'interests': data.get('interests', ''),
            'notes': data.get('notes', ''),
            'plan': current_user.plan,
            'budget_friendly': data.get('budgetFriendly', False)
        }
        
        # Calculate days from dates
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        ai_input_data['days'] = (end_date - start_date).days + 1
        
        print(f"🎯 Generating {ai_input_data['days']}-day itinerary with AI...")
        print(f"📊 Final AI input data - Plan: {ai_input_data['plan']}")
        
        # Use appropriate AI model based on plan
        if AI_AVAILABLE:
            if ai_input_data['plan'] == 'pro':
                print(f"🚀 Using PRO AI model for pro plan itinerary generation")
                # Initialize pro model if not already done
                if not hasattr(generate_itinerary, 'pro_model'):
                    try:
                        from pro_model_config import TripStarProModel
                        generate_itinerary.pro_model = TripStarProModel()
                        print("✅ Pro AI model initialized successfully")
                    except ImportError as e:
                        print(f"❌ Pro AI model not available: {e}")
                        generate_itinerary.pro_model = None
                
                # Use pro model if available, otherwise fall back to basic model
                if generate_itinerary.pro_model and generate_itinerary.pro_model.client:
                    itinerary = generate_itinerary.pro_model.generate_itinerary(ai_input_data)
                elif ai_model and ai_model.client:
                    print("⚠️ Pro model not available, using basic AI model")
                    itinerary = ai_model.generate_itinerary(ai_input_data)
                else:
                    print("⚠️ No AI models available, using template itinerary")
                    itinerary = generate_fallback_itinerary(ai_input_data)
            else:
                # Free plan uses basic AI model
                print(f"🆓 Using basic AI model for free plan itinerary generation")
                if ai_model and ai_model.client:
                    itinerary = ai_model.generate_itinerary(ai_input_data)
                else:
                    print("⚠️ AI model not available, using template itinerary")
                    itinerary = generate_fallback_itinerary(ai_input_data)
        else:
            print("⚠️ AI not available, using template itinerary")
            itinerary = generate_fallback_itinerary(ai_input_data)
        
        if itinerary:
            # Save itinerary to database
            new_itinerary = Itinerary(
                user_id=current_user.id,
                title=f"{data['destinations'][0]} Itinerary",
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
            
            logger.info(f"Itinerary generated and saved successfully for {current_user.email}")
            
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
    interests = data.get('interests', 'General sightseeing')
    
    destination_name = destinations[0] if destinations else "your destination"
    
    itinerary = {
        "days": [],
        "popularSpots": [
            {
                "name": f"{destination_name} Historic Center",
                "description": f"Explore the cultural heart of {destination_name} with stunning architecture dating back centuries."
            },
            {
                "name": "Local Food Markets", 
                "description": f"Experience authentic culinary traditions at {destination_name}'s bustling local markets."
            }
        ],
        "summary": f"This {days}-day journey through {destination_name} is designed for {traveler_type.lower()} travelers with a {currency_symbol}{budget} budget."
    }
    
    # Generate day-by-day itinerary
    for day in range(1, days + 1):
        if day == 1:
            itinerary["days"].append({
                "day": day,
                "title": f"Welcome to {destination_name}",
                "description": f"Your adventure begins with an introduction to {destination_name}'s rich cultural heritage.",
                "activities": [
                    f"Morning: Arrive in {destination_name} and check into accommodation",
                    f"Afternoon: Orientation walk through the main historical area",
                    f"Evening: Welcome dinner at a traditional restaurant"
                ],
                "tip": "Take time to absorb the local atmosphere and observe daily life patterns."
            })
        elif day == days:
            itinerary["days"].append({
                "day": day,
                "title": "Final Explorations",
                "description": "Make the most of your last hours with final explorations.",
                "activities": [
                    "Morning: Last-minute souvenir shopping at local markets",
                    "Afternoon: Revisit your favorite spot",
                    "Evening: Airport transfer and departure"
                ],
                "tip": "Pack main luggage the night before to allow time for final observations."
            })
        else:
            itinerary["days"].append({
                "day": day,
                "title": f"Day {day} Adventures",
                "description": f"Explore more of {destination_name}'s unique character and traditions.",
                "activities": [
                    "Morning: Guided exploration of cultural sites",
                    "Afternoon: Hands-on local experience",
                    "Evening: Free time to wander and dine locally"
                ],
                "tip": "Wear comfortable shoes and carry a refillable water bottle."
            })
    
    return itinerary

@app.route('/test-ai')
def test_ai():
    """Test route to verify AI model is working"""
    if not AI_AVAILABLE or not ai_model or not ai_model.client:
        return jsonify({'status': 'AI not available'})
    
    try:
        # Test with sample data
        test_data = {
            'user_name': 'Test User',
            'destinations': ['France'],
            'start_date': '2025-01-01',
            'end_date': '2025-01-03',
            'traveler_type': 'Solo',
            'budget': 2000,
            'currency_symbol': '$',
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
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

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
            return jsonify({'interests': list(all_interests)[:12]})  # Limit to 12 interests
        
        # Use AI to generate relevant interests
        destinations_str = ', '.join(destinations)
        prompt = f"""Based on these travel destinations: {destinations_str}
        
        Suggest 12-15 most relevant travel interest categories that would appeal to various types of travelers. 
        Return ONLY a JSON array of strings, no explanations.
        
        Example: ["Historical Sites", "Local Cuisine", "Adventure Sports", "Art Museums", "Beach Activities", "Nightlife", "Shopping", "Nature & Parks", "Cultural Experiences", "Wellness & Spas", "Family Activities", "Photography Spots"]
        
        Focus on interests that are most relevant to the specific destinations mentioned."""
        
        response = ai_model.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel expert. Respond with ONLY a JSON array of strings, no other text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=ai_model.model_name,
            temperature=0.7,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Parse the response
        try:
            interests = json.loads(response_text)
            if isinstance(interests, list):
                return jsonify({'interests': interests})
        except json.JSONDecodeError:
            print("Failed to parse AI interests response")
        
        # Fallback if AI fails
        all_interests = set()
        for destination in destinations:
            interests = countryInterests.get(destination, countryInterests['default'])
            all_interests.update(interests)
        return jsonify({'interests': list(all_interests)[:12]})
        
    except Exception as e:
        logger.error(f"Error getting AI interests: {str(e)}")
        # Fallback to static interests
        all_interests = set()
        for destination in destinations:
            interests = countryInterests.get(destination, countryInterests['default'])
            all_interests.update(interests)
        return jsonify({'interests': list(all_interests)[:12]})

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('static', filename)

@app.route('/payment')
@login_required
def payment_page():
    """Payment page for upgrading to pro"""
    return render_template('payment.html')

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
    # Clear session cookie
    from flask import session
    session.clear()
    return redirect(url_for('welcome'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)