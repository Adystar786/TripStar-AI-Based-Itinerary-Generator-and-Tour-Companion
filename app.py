from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import os
from payment_models import Payment
from datetime import datetime, timedelta
import logging
import uuid
from flask import request, jsonify, render_template
from models import db, User, Itinerary, UsageRecord
import qrcode
from io import BytesIO
import base64
import re

with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")

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
        
        # Import Payment model
        from payment_models import Payment
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
        
        from payment_models import Payment
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
    """Verify payment - requires manual admin approval"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        transaction_id = data.get('transaction_id')
        
        if not transaction_id:
            return jsonify({'success': False, 'error': 'Transaction ID is required'}), 400
        
        from payment_models import Payment
        payment = Payment.query.filter_by(payment_id=payment_id, user_id=current_user.id).first()
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment record not found'}), 404
        
        # Store transaction ID but DON'T auto-approve
        payment.transaction_id = transaction_id
        payment.status = 'pending_verification'  # Changed from 'completed'
        db.session.commit()
        
        # Send notification email to admin (you)
        send_payment_notification_email(current_user, payment, transaction_id)
        
        logger.info(f"Payment verification pending - User: {current_user.email}, Transaction: {transaction_id}")
        
        return jsonify({
            'success': True,
            'message': 'Payment submitted for verification. You will be upgraded within 2-4 hours after we verify your payment. Check your email for updates.',
            'pending': True  # Important: tells frontend it's not instant
        })
        
    except Exception as e:
        logger.error(f"Payment verification error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Payment verification failed'}), 500

@app.route('/payment/manual-verification', methods=['POST'])
@login_required
def manual_verification():
    """Manual payment verification - requires admin approval"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        user_upi_id = data.get('upi_id')
        amount = data.get('amount')
        
        if not user_upi_id:
            return jsonify({'success': False, 'error': 'UPI ID is required'}), 400
        
        from payment_models import Payment
        payment = Payment.query.filter_by(payment_id=payment_id, user_id=current_user.id).first()
        
        if payment:
            payment.upi_id = user_upi_id
            payment.status = 'manual_verification_pending'  # Changed status
            db.session.commit()
        
        # Send notification to admin
        send_manual_verification_email(current_user, payment_id, user_upi_id, amount)
        
        logger.info(f"Manual verification requested - User: {current_user.email}, Payment: {payment_id}, UPI: {user_upi_id}")
        
        # NO AUTO-APPROVAL - removed the auto-upgrade code
        return jsonify({
            'success': True,
            'message': 'Manual verification request submitted. We will verify your payment within 24 hours and upgrade your account. You will receive an email confirmation.',
            'contact_email': 'adystar67@gmail.com',
            'pending': True
        })
        
    except Exception as e:
        logger.error(f"Manual verification error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Manual verification request failed'}), 500

# Add admin route to approve payments
@app.route('/admin/payments')
@login_required
def admin_payments():
    """Admin page to view and approve payments"""
    # Add admin check here
    if current_user.email != 'adystar67@gmail.com':  # Your admin email
        return redirect(url_for('dashboard'))
    
    from payment_models import Payment
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
        from payment_models import Payment
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
        
        # Send confirmation email to user
        send_upgrade_confirmation_email(user)
        
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
        from payment_models import Payment
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'success': False, 'error': 'Payment not found'}), 404
        
        data = request.get_json()
        reason = data.get('reason', 'Payment verification failed')
        
        payment.status = 'rejected'
        db.session.commit()
        
        # Send rejection email to user
        user = User.query.get(payment.user_id)
        send_rejection_email(user, reason)
        
        logger.info(f"Payment rejected by admin - User: {user.email}, Reason: {reason}")
        
        return jsonify({'success': True, 'message': 'Payment rejected'})
        
    except Exception as e:
        logger.error(f"Payment rejection error: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Email notification functions
def send_payment_notification_email(user, payment, transaction_id):
    """Send email to admin about new payment"""
    subject = f"New Payment Verification - {user.email}"
    body = f"""
    New payment verification request:
    
    User: {user.first_name} {user.last_name}
    Email: {user.email}
    Payment ID: {payment.payment_id}
    Transaction ID: {transaction_id}
    Amount: ₹{payment.amount}
    
    Verify at: http://yoursite.com/admin/payments
    """
    
    # Implement actual email sending here (using Flask-Mail, SendGrid, etc.)
    logger.info(f"Payment notification email: {subject}")
    print(body)  # For testing

def send_manual_verification_email(user, payment_id, upi_id, amount):
    """Send email to admin about manual verification request"""
    subject = f"Manual Payment Verification - {user.email}"
    body = f"""
    Manual payment verification request:
    
    User: {user.first_name} {user.last_name}
    Email: {user.email}
    Payment ID: {payment_id}
    User's UPI ID: {upi_id}
    Amount: ₹{amount}
    
    Check your UPI transaction history for payment from: {upi_id}
    Verify at: http://yoursite.com/admin/payments
    """
    
    logger.info(f"Manual verification email: {subject}")
    print(body)  # For testing

def send_upgrade_confirmation_email(user):
    """Send confirmation email to user after upgrade"""
    subject = "Welcome to TripStar AI Pro!"
    body = f"""
    Hi {user.first_name},
    
    Your payment has been verified and your account has been upgraded to PRO! 🎉
    
    You now have:
    ✅ Unlimited AI itinerary generation
    ✅ Premium features
    ✅ Priority support
    
    Start creating amazing itineraries: http://yoursite.com/dashboard
    
    Thanks for upgrading!
    TripStar AI Team
    """
    
    logger.info(f"Upgrade confirmation email sent to: {user.email}")
    print(body)  # For testing

def send_rejection_email(user, reason):
    """Send rejection email to user"""
    subject = "Payment Verification Issue - TripStar AI"
    body = f"""
    Hi {user.first_name},
    
    We were unable to verify your payment.
    
    Reason: {reason}
    
    If you believe this is an error, please contact us at adystar67@gmail.com
    with your transaction details.
    
    TripStar AI Team
    """
    
    logger.info(f"Rejection email sent to: {user.email}")
    print(body)  # For testing

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
        logger.info(f"Destinations received: {data.get('destinations')}")
        logger.info(f"Destination codes received: {data.get('destinationCodes')}")
        
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
            'destination_codes': data.get('destinationCodes', []),  # ADD THIS
            'start_date': data['startDate'],
            'end_date': data['endDate'],
            'traveler_type': data['travelerType'],
            'budget': float(data['budget']),
            'currency_symbol': data.get('currencySymbol', '$'),
            'interests': data.get('interests', ''),
            'notes': data.get('notes', ''),
            'plan': current_user.plan,
            'budget_friendly': data.get('budgetFriendly', False),
            'departure_city': data.get('departureCity', ''),  # ADD THIS
            'departure_city_code': data.get('departureCityCode', '')  # ADD THIS
        }
        
        # Calculate days from dates
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        ai_input_data['days'] = (end_date - start_date).days + 1
        
        print(f"🎯 Generating {ai_input_data['days']}-day itinerary for {len(data['destinations'])} destinations with AI...")
        print(f"📊 Destinations: {', '.join(data['destinations'])}")
        
        # Use appropriate AI model based on plan
        if AI_AVAILABLE:
            if ai_input_data['plan'] == 'pro':
                print(f"🚀 Using PRO AI model for pro plan itinerary generation")
                if not hasattr(generate_itinerary, 'pro_model'):
                    try:
                        from pro_model_config import TripStarProModel
                        generate_itinerary.pro_model = TripStarProModel()
                        print("✅ Pro AI model initialized successfully")
                    except ImportError as e:
                        print(f"❌ Pro AI model not available: {e}")
                        generate_itinerary.pro_model = None
                
                if generate_itinerary.pro_model and generate_itinerary.pro_model.client:
                    itinerary = generate_itinerary.pro_model.generate_itinerary(ai_input_data)
                elif ai_model and ai_model.client:
                    print("⚠️ Pro model not available, using basic AI model")
                    itinerary = ai_model.generate_itinerary(ai_input_data)
                else:
                    print("⚠️ No AI models available, using template itinerary")
                    itinerary = generate_fallback_itinerary(ai_input_data)
            else:
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
                title=f"{', '.join(data['destinations'])} Itinerary",  # UPDATED
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
            
            # Add emojis to interests
            interests_with_emojis = add_emojis_to_interests(list(all_interests)[:15])
            return jsonify({'interests': interests_with_emojis})
        
        # Use AI to generate relevant interests
        destinations_str = ', '.join(destinations)
        prompt = f"""Based on these travel destinations: {destinations_str}
        
        Suggest 15 most relevant travel interest categories that would appeal to various types of travelers visiting ALL of these destinations. 
        Consider unique activities and experiences available across all mentioned locations.
        Return ONLY a JSON array of strings, no explanations, no emojis.
        
        Example format: ["Historical Sites", "Local Cuisine", "Adventure Sports", "Art Museums", "Beach Activities", "Nightlife", "Shopping", "Nature & Parks", "Cultural Experiences", "Wellness & Spas", "Family Activities", "Photography Spots", "Wildlife Viewing", "Water Sports", "Mountain Hiking"]
        
        Focus on interests that are most relevant to the specific destinations: {destinations_str}"""
        
        response = ai_model.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a travel expert. Respond with ONLY a JSON array of strings, no other text, no emojis."
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
                # Add emojis to interests
                interests_with_emojis = add_emojis_to_interests(interests)
                return jsonify({'interests': interests_with_emojis})
        except json.JSONDecodeError:
            print("Failed to parse AI interests response")
        
        # Fallback if AI fails
        all_interests = set()
        for destination in destinations:
            interests = countryInterests.get(destination, countryInterests['default'])
            all_interests.update(interests)
        
        interests_with_emojis = add_emojis_to_interests(list(all_interests)[:15])
        return jsonify({'interests': interests_with_emojis})
        
    except Exception as e:
        logger.error(f"Error getting AI interests: {str(e)}")
        # Fallback to static interests
        all_interests = set()
        for destination in destinations:
            interests = countryInterests.get(destination, countryInterests['default'])
            all_interests.update(interests)
        
        interests_with_emojis = add_emojis_to_interests(list(all_interests)[:15])
        return jsonify({'interests': interests_with_emojis})

def add_emojis_to_interests(interests):
    """Add relevant emojis to interest categories"""
    emoji_map = {
        'historical': '🏛️', 'history': '🏛️', 'monument': '🏛️', 'sites': '🏛️',
        'food': '🍽️', 'cuisine': '🍽️', 'dining': '🍽️', 'culinary': '🍽️',
        'beach': '🏖️', 'coast': '🏖️', 'seaside': '🏖️',
        'art': '🎨', 'museum': '🎨', 'gallery': '🎨',
        'shopping': '🛍️', 'market': '🛍️',
        'nature': '🌿', 'park': '🌿', 'garden': '🌿',
        'adventure': '🏔️', 'hiking': '🏔️', 'trekking': '🏔️', 'mountain': '🏔️',
        'water': '🌊', 'diving': '🌊', 'snorkeling': '🌊',
        'wildlife': '🦁', 'safari': '🦁', 'animal': '🦁',
        'culture': '🎭', 'cultural': '🎭', 'traditional': '🎭',
        'nightlife': '🌃', 'club': '🌃', 'party': '🌃',
        'wellness': '🧘', 'spa': '🧘', 'yoga': '🧘', 'meditation': '🧘',
        'photo': '📸', 'photography': '📸',
        'wine': '🍷', 'tasting': '🍷',
        'temple': '🛕', 'shrine': '🛕', 'spiritual': '🛕',
        'family': '👨‍👩‍👧‍👦', 'kids': '👨‍👩‍👧‍👦', 'children': '👨‍👩‍👧‍👦',
        'romantic': '💑', 'couple': '💑',
        'sport': '⚽', 'activity': '⚽', 'activities': '⚽',
        'architecture': '🏗️', 'building': '🏗️',
        'cruise': '🚢', 'boat': '🚢',
        'festival': '🎉', 'event': '🎉',
        'cooking': '👨‍🍳', 'class': '👨‍🍳',
        'island': '🏝️', 'hopping': '🏝️',
        'city': '🌆', 'urban': '🌆', 'tour': '🌆',
        'castle': '🏰', 'palace': '🏰',
        'music': '🎵', 'concert': '🎵',
        'local': '🏘️', 'authentic': '🏘️'
    }
    
    interests_with_emojis = []
    for interest in interests:
        emoji = '🎯'  # Default emoji
        interest_lower = interest.lower()
        
        # Find matching emoji
        for keyword, mapped_emoji in emoji_map.items():
            if keyword in interest_lower:
                emoji = mapped_emoji
                break
        
        interests_with_emojis.append(f"{interest} {emoji}")
    
    return interests_with_emojis

@app.route('/search-flights', methods=['POST'])
@login_required
def search_flights():
    """Search for best flights for the itinerary with enhanced error handling"""
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
        
        # Validate required parameters
        if not departure_city or not destinations or not start_date or not end_date:
            logger.warning("Missing required flight search parameters")
            return jsonify({
                'success': False, 
                'error': 'Missing required parameters: departure city, destinations, and dates are required'
            }), 400
        
        # Ensure destinations is a list and not empty
        if not isinstance(destinations, list) or len(destinations) == 0:
            logger.warning("Invalid destinations format")
            return jsonify({
                'success': False,
                'error': 'Invalid destinations format'
            }), 400
        
        logger.info(f"Flight search: {departure_city} → {', '.join(destinations)}")
        
        # Use AI for Pro users, fallback for free users
        flight_results = None
        if current_user.plan == 'pro' and AI_AVAILABLE and ai_model and ai_model.client:
            try:
                logger.info("Using AI for Pro user flight search")
                flight_results = search_flights_with_ai(
                    departure_city, departure_city_code, destinations, destination_codes,
                    start_date, end_date, budget, currency_symbol
                )
            except Exception as ai_err:
                logger.error(f"AI search failed: {ai_err}")
                flight_results = generate_fallback_flights(
                    departure_city, departure_city_code, destinations, destination_codes,
                    start_date, end_date, budget, currency_symbol
                )
        else:
            logger.info("Using fallback flight search")
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
            'error': 'Flight search failed due to technical issues'
        }), 500

def search_flights_with_ai(departure_city, departure_city_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol):
    """Use AI to search and recommend REAL flights based on actual routing"""
    try:
        # Validate input data
        if not destinations or len(destinations) == 0:
            return generate_fallback_flights(departure_city, departure_city_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol)
        
        # Ensure destination_codes matches destinations
        if not destination_codes or len(destination_codes) != len(destinations):
            destination_codes = [dest.split(',')[0] if ',' in dest else dest for dest in destinations]
        
        print(f"🎯 Generating REAL flight data for: {departure_city} → {', '.join(destinations)}")
        
        # Build dynamic prompt based on actual destinations
        if len(destinations) > 1:
            # Multi-city itinerary
            route_description = f"{departure_city} → " + " → ".join(destinations) + f" → {departure_city}"
            
            prompt = f"""Generate REAL flight recommendations for this multi-city trip:

ACTUAL ITINERARY:
- Departure: {departure_city}
- Route: {route_description}
- Travel Dates: {start_date} to {end_date}
- Budget: {currency_symbol}{budget}
- Destinations: {', '.join(destinations)}

Provide SPECIFIC, REALISTIC flight options for each segment. Use ACTUAL airline names and realistic pricing.

IMPORTANT: Return ONLY valid JSON. Be specific and realistic.

{{
  "flights": [
    {{
      "segment": "Outbound",
      "departureCity": "{departure_city}",
      "destination": "{destinations[0]}",
      "outboundDate": "{start_date}",
      "returnDate": "{end_date}",
      "options": [
        {{
          "airline": "Singapore Airlines",
          "flightNumber": "SQ 508",
          "duration": "4h 15m",
          "stops": 0,
          "layover": "None",
          "cabinClasses": {{
            "economy": {{"price": "{currency_symbol}{int(budget * 0.12)}", "available": true, "seatsLeft": "12"}},
            "premiumEconomy": {{"price": "{currency_symbol}{int(budget * 0.18)}", "available": true, "seatsLeft": "6"}},
            "business": {{"price": "{currency_symbol}{int(budget * 0.25)}", "available": true, "seatsLeft": "3"}}
          }},
          "moneySavingTips": [
            "Book 2 months in advance for 20% savings",
            "Consider mid-week flights for better prices"
          ]
        }},
        {{
          "airline": "AirAsia",
          "flightNumber": "AK 101",
          "duration": "4h 30m", 
          "stops": 0,
          "layover": "None",
          "cabinClasses": {{
            "economy": {{"price": "{currency_symbol}{int(budget * 0.08)}", "available": true, "seatsLeft": "25"}},
            "premiumEconomy": {{"price": "{currency_symbol}{int(budget * 0.12)}", "available": true, "seatsLeft": "8"}}
          }},
          "moneySavingTips": [
            "Book directly on airline website for no fees",
            "Add baggage during booking for discount"
          ]
        }}
      ]
    }},
    {{
      "segment": "Intermediate",
      "departureCity": "{destinations[0]}",
      "destination": "{destinations[1]}",
      "outboundDate": "Add 3-4 days after arrival",
      "returnDate": "{end_date}",
      "options": [
        {{
          "airline": "Malaysia Airlines",
          "flightNumber": "MH 612",
          "duration": "2h 15m",
          "stops": 0,
          "layover": "None",
          "cabinClasses": {{
            "economy": {{"price": "{currency_symbol}{int(budget * 0.06)}", "available": true, "seatsLeft": "18"}},
            "business": {{"price": "{currency_symbol}{int(budget * 0.15)}", "available": true, "seatsLeft": "4"}}
          }},
          "moneySavingTips": [
            "Regional flights cheaper when booked with main itinerary",
            "Check for airline combo deals"
          ]
        }}
      ]
    }},
    {{
      "segment": "Return",
      "departureCity": "{destinations[-1]}",
      "destination": "{departure_city}",
      "outboundDate": "{end_date}",
      "returnDate": "{end_date}",
      "options": [
        {{
          "airline": "Emirates",
          "flightNumber": "EK 568",
          "duration": "5h 20m",
          "stops": 0,
          "layover": "None", 
          "cabinClasses": {{
            "economy": {{"price": "{currency_symbol}{int(budget * 0.15)}", "available": true, "seatsLeft": "9"}},
            "premiumEconomy": {{"price": "{currency_symbol}{int(budget * 0.22)}", "available": true, "seatsLeft": "5"}},
            "business": {{"price": "{currency_symbol}{int(budget * 0.35)}", "available": true, "seatsLeft": "2"}}
          }},
          "moneySavingTips": [
            "Return flights cheaper when booked round-trip",
            "Flexible dates can save 30%"
          ]
        }}
      ]
    }}
  ],
  "searchLink": "https://www.google.com/travel/flights",
  "generalTips": [
    "Book multi-city as single itinerary for best pricing",
    "Allow minimum 3 days in each destination",
    "Verify visa requirements for all transit points",
    "Check COVID-19 travel restrictions if applicable"
  ]
}}"""
        else:
            # Single destination
            destination = destinations[0]
            prompt = f"""Generate REAL flight recommendations:

ACTUAL TRIP:
- From: {departure_city} 
- To: {destination}
- Dates: {start_date} to {end_date}
- Budget: {currency_symbol}{budget}

Provide SPECIFIC, REALISTIC flight options with actual airline names and realistic pricing.

{{
  "flights": [
    {{
      "departureCity": "{departure_city}",
      "destination": "{destination}",
      "outboundDate": "{start_date}",
      "returnDate": "{end_date}",
      "options": [
        {{
          "airline": "Qatar Airways",
          "flightNumber": "QR 102",
          "duration": "3h 45m",
          "stops": 0,
          "layover": "None",
          "cabinClasses": {{
            "economy": {{"price": "{currency_symbol}{int(budget * 0.25)}", "available": true, "seatsLeft": "15"}},
            "premiumEconomy": {{"price": "{currency_symbol}{int(budget * 0.38)}", "available": true, "seatsLeft": "7"}},
            "business": {{"price": "{currency_symbol}{int(budget * 0.65)}", "available": true, "seatsLeft": "3"}}
          }},
          "moneySavingTips": [
            "Book 6-8 weeks in advance for optimal pricing",
            "Consider flying on Tuesday/Wednesday for 20% savings"
          ]
        }},
        {{
          "airline": "IndiGo",
          "flightNumber": "6E 87",
          "duration": "4h 10m",
          "stops": 0,
          "layover": "None",
          "cabinClasses": {{
            "economy": {{"price": "{currency_symbol}{int(budget * 0.18)}", "available": true, "seatsLeft": "22"}},
            "premiumEconomy": {{"price": "{currency_symbol}{int(budget * 0.28)}", "available": true, "seatsLeft": "10"}}
          }},
          "moneySavingTips": [
            "Low-cost carrier with competitive pricing",
            "Book baggage allowance in advance"
          ]
        }}
      ],
      "bestDeal": {{
        "airline": "IndiGo",
        "class": "Economy",
        "price": "{currency_symbol}{int(budget * 0.18)}",
        "why": "Best value low-cost carrier with good availability"
      }}
    }}
  ],
  "searchLink": "https://www.google.com/travel/flights",
  "generalTips": [
    "Book round-trip for better pricing than one-way",
    "Be flexible with dates for significant savings",
    "Check both direct and connecting flight options",
    "Verify baggage allowances before booking"
  ]
}}"""

        if not AI_AVAILABLE or not ai_model or not ai_model.client:
            print("⚠️ AI not available, using enhanced fallback flights")
            return generate_dynamic_fallback_flights(departure_city, departure_city_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol)

        response = ai_model.client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a flight booking expert. Provide SPECIFIC, REALISTIC flight information with actual airline names, realistic pricing, and practical tips. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=ai_model.model_name,
            temperature=0.7,
            max_tokens=4000
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"📝 AI Flight Response: {response_text[:500]}...")  # Debug log
        
        # Clean and parse response
        response_text = response_text.replace('```json', '').replace('```', '').strip()
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            response_text = response_text[start_idx:end_idx+1]
        
        response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)
        
        try:
            flight_data = json.loads(response_text)
            print("✅ Successfully parsed dynamic flight data")
        except json.JSONDecodeError as json_err:
            print(f"❌ JSON parse error: {json_err}")
            print("🔄 Using enhanced fallback flights")
            return generate_dynamic_fallback_flights(departure_city, departure_city_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol)
        
        # Add actual booking links based on real routes
        if 'flights' in flight_data and isinstance(flight_data['flights'], list):
            for flight in flight_data['flights']:
                if isinstance(flight, dict):
                    dep_city = flight.get('departureCity', departure_city)
                    dest_city = flight.get('destination', destinations[0] if destinations else '')
                    
                    for option in flight.get('options', []):
                        if isinstance(option, dict):
                            # Create actual Google Flights search URL
                            option['bookingLink'] = create_flight_search_url(dep_city, dest_city, start_date, end_date)
        
        # Add main search link
        if len(destinations) > 1:
            flight_data['searchLink'] = create_multicity_flight_url(departure_city_code, destination_codes, start_date, end_date)
        else:
            flight_data['searchLink'] = create_flight_search_url(departure_city, destinations[0], start_date, end_date)
        
        return flight_data
        
    except Exception as e:
        print(f"❌ AI flight search error: {str(e)}")
        return generate_dynamic_fallback_flights(departure_city, departure_city_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol)
    
def generate_fallback_flights(departure_city, departure_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol):
    """Generate fallback flight recommendations with proper error handling"""
    
    # Validate and sanitize inputs
    if not destinations or len(destinations) == 0:
        logger.error("No destinations provided for fallback flights")
        return {"flights": [], "searchLink": "#", "generalTips": ["Please select destinations to see flight options"]}
    
    # Ensure destination_codes matches destinations length
    if not destination_codes or len(destination_codes) != len(destinations):
        destination_codes = []
        for dest in destinations:
            # Extract city name from "City, Country" format or use as-is
            if ',' in dest:
                city = dest.split(',')[0].strip()
                destination_codes.append(city[:3].upper() if len(city) >= 3 else city.upper())
            else:
                destination_codes.append(dest[:3].upper() if len(dest) >= 3 else dest.upper())
    
    flights = []
    
    # If multiple destinations, create multi-city route
    if len(destinations) > 1:
        route_description = f"{departure_city}"
        for dest in destinations:
            route_description += f" → {dest}"
        route_description += f" → {departure_city}"
        
        # Main multi-city flight option
        flights.append({
            "routeType": "multi-city",
            "route": route_description,
            "departureCity": departure_city,
            "departureCode": departure_code,
            "destinations": destinations,
            "destinationCodes": destination_codes,
            "outboundDate": start_date,
            "returnDate": end_date,
            "options": [
                {
                    "airline": "Multiple Airlines",
                    "flightNumber": "Multi-city booking required",
                    "cabinClasses": {
                        "economy": {
                            "price": f"{currency_symbol}{int(budget * 0.4)}",
                            "available": True,
                            "seatsLeft": "Available"
                        },
                        "business": {
                            "price": f"{currency_symbol}{int(budget * 0.7)}",
                            "available": True,
                            "seatsLeft": "Limited"
                        }
                    },
                    "duration": "Varies by route",
                    "stops": "Multiple segments",
                    "layover": "Between cities",
                    "bookingLink": create_multicity_flight_url(departure_code, destination_codes, start_date, end_date),
                    "moneySavingTips": [
                        "Book all segments together for better pricing",
                        "Consider open-jaw tickets",
                        "Use multi-city booking tools",
                        "Be flexible with dates"
                    ]
                }
            ],
            "bestDeal": {
                "airline": "Budget Airlines Combination",
                "class": "Economy",
                "price": f"{currency_symbol}{int(budget * 0.35)}",
                "why": "Book individual segments separately"
            }
        })
        
        # Individual leg details
        for i, destination in enumerate(destinations):
            dest_code = destination_codes[i] if i < len(destination_codes) else ""
            
            # Determine departure for this segment
            if i == 0:
                segment_departure = departure_city
                segment_departure_code = departure_code
            else:
                segment_departure = destinations[i-1]
                segment_departure_code = destination_codes[i-1] if i-1 < len(destination_codes) else ""
            
            flights.append({
                "segment": f"Leg {i+1}",
                "destination": destination,
                "destinationCode": dest_code,
                "departureCity": segment_departure,
                "departureCode": segment_departure_code,
                "options": [
                    {
                        "airline": "Various Airlines",
                        "flightNumber": "Check availability",
                        "cabinClasses": {
                            "economy": {
                                "price": f"{currency_symbol}{int(budget * 0.15)}",
                                "available": True
                            }
                        },
                        "duration": "Varies",
                        "stops": "0-1",
                        "bookingLink": create_flight_search_url(segment_departure, destination, start_date, end_date),
                        "moneySavingTips": [
                            f"Book {segment_departure} to {destination} separately"
                        ]
                    }
                ]
            })
        
        # Return flight
        flights.append({
            "segment": f"Return Flight",
            "destination": departure_city,
            "destinationCode": departure_code,
            "departureCity": destinations[-1],
            "departureCode": destination_codes[-1] if destination_codes else "",
            "options": [
                {
                    "airline": "Various Airlines",
                    "bookingLink": create_flight_search_url(destinations[-1], departure_city, end_date, end_date),
                    "moneySavingTips": [
                        "Book return flight early for best rates"
                    ]
                }
            ]
        })
        
    else:
        # Single destination
        destination = destinations[0]
        dest_code = destination_codes[0] if destination_codes else ""
        
        flights.append({
            "routeType": "round-trip",
            "destination": destination,
            "destinationCode": dest_code,
            "departureCity": departure_city,
            "departureCode": departure_code,
            "outboundDate": start_date,
            "returnDate": end_date,
            "options": [
                {
                    "airline": "Major Airlines",
                    "flightNumber": "Multiple options",
                    "cabinClasses": {
                        "economy": {
                            "price": f"{currency_symbol}{int(budget * 0.3)}",
                            "available": True,
                            "seatsLeft": "Available"
                        },
                        "business": {
                            "price": f"{currency_symbol}{int(budget * 0.7)}",
                            "available": True
                        }
                    },
                    "duration": "Varies",
                    "stops": "0-2",
                    "bookingLink": create_flight_search_url(departure_city, destination, start_date, end_date),
                    "moneySavingTips": [
                        "Book 6-8 weeks in advance",
                        "Consider nearby airports",
                        "Use incognito mode when searching"
                    ]
                }
            ]
        })
    
    return {
        "flights": flights,
        "searchLink": create_multicity_flight_url(departure_code, destination_codes, start_date, end_date) if len(destinations) > 1 else create_flight_search_url(departure_city, destinations[0], start_date, end_date),
        "generalTips": [
            "For multi-city trips, compare different booking strategies",
            "Book flights 6-8 weeks in advance for best prices",
            "Be flexible with dates to save up to 40%",
            "Consider budget airlines for shorter segments",
            "Check baggage policies carefully"
        ]
    }

def create_multicity_flight_url(departure_code, destination_codes, start_date, end_date):
    """Create Google Flights multi-city search URL with error handling"""
    from urllib.parse import quote
    
    try:
        if not destination_codes or len(destination_codes) == 0:
            return "https://www.google.com/travel/flights"
            
        if len(destination_codes) > 1:
            # Build basic multi-city search
            route_str = f"{departure_code}-{destination_codes[0]}" if departure_code else f"to-{destination_codes[0]}"
            for i in range(1, len(destination_codes)):
                route_str += f"-{destination_codes[i]}"
            route_str += f"-{departure_code}" if departure_code else ""
            
            return f"https://www.google.com/travel/flights?q=Multi-city%20flights%20{quote(route_str)}"
        else:
            # Single destination
            dest = destination_codes[0] if destination_codes else ""
            return f"https://www.google.com/travel/flights?q=Flights%20to%20{quote(dest)}"
    except Exception as e:
        logger.error(f"Error creating multi-city URL: {e}")
        return "https://www.google.com/travel/flights"

def create_flight_search_url(departure, destination, start_date, end_date):
    """Create Google Flights deep link with search parameters"""
    from urllib.parse import quote
    
    # Extract city names from "City, Country" format
    dep_city = departure.split(',')[0].strip() if ',' in departure else departure
    dest_city = destination.split(',')[0].strip() if ',' in destination else destination
    
    # Google Flights URL format
    return f"https://www.google.com/travel/flights?q=Flights%20to%20{quote(dest_city)}%20from%20{quote(dep_city)}%20on%20{start_date}%20returning%20{end_date}"

def generate_dynamic_fallback_flights(departure_city, departure_code, destinations, destination_codes, start_date, end_date, budget, currency_symbol):
    """Generate dynamic fallback flights based on actual destinations"""
    
    if not destinations or len(destinations) == 0:
        return {"flights": [], "searchLink": "#", "generalTips": ["Select destinations to see flight options"]}
    
    # Common airlines by region
    airlines = {
        'asia': ['Singapore Airlines', 'Thai Airways', 'Malaysia Airlines', 'AirAsia', 'IndiGo', 'Emirates', 'Qatar Airways'],
        'europe': ['Lufthansa', 'British Airways', 'Air France', 'KLM', 'Turkish Airlines', 'Swiss International'],
        'america': ['United Airlines', 'Delta', 'American Airlines', 'Air Canada', 'Latam Airlines'],
        'middle_east': ['Emirates', 'Qatar Airways', 'Etihad Airways', 'Saudia']
    }
    
    flights = []
    
    if len(destinations) > 1:
        # Multi-city routing
        for i, destination in enumerate(destinations):
            if i == 0:
                # First leg: departure to first destination
                segment_data = create_flight_segment(
                    departure_city, destination, start_date, budget, currency_symbol, 
                    airlines['asia'], "Outbound", i
                )
            elif i < len(destinations):
                # Intermediate legs
                prev_dest = destinations[i-1]
                segment_data = create_flight_segment(
                    prev_dest, destination, f"Day {i+2}", budget, currency_symbol,
                    airlines['asia'], f"Leg {i+1}", i
                )
            
            if segment_data:
                flights.append(segment_data)
        
        # Return leg
        return_segment = create_flight_segment(
            destinations[-1], departure_city, end_date, budget, currency_symbol,
            airlines['asia'], "Return", len(destinations)
        )
        if return_segment:
            flights.append(return_segment)
            
    else:
        # Single destination
        destination = destinations[0]
        flight_data = create_flight_segment(
            departure_city, destination, start_date, budget, currency_symbol,
            airlines['asia'], "Round-trip", 0
        )
        if flight_data:
            flights.append(flight_data)
    
    return {
        "flights": flights,
        "searchLink": create_multicity_flight_url(departure_code, destination_codes, start_date, end_date) if len(destinations) > 1 else create_flight_search_url(departure_city, destinations[0], start_date, end_date),
        "generalTips": [
            f"Book your {len(destinations)}-destination trip 2-3 months in advance",
            "Compare multi-city vs individual booking prices",
            "Check visa requirements for all destinations",
            "Allow sufficient connection time between flights"
        ]
    }

def create_flight_segment(departure, destination, date, budget, currency_symbol, airline_list, segment_name, index):
    """Create a realistic flight segment"""
    base_price = int(budget * (0.1 + (index * 0.05)))  # Dynamic pricing based on segment
    
    return {
        "segment": segment_name,
        "departureCity": departure,
        "destination": destination,
        "outboundDate": date,
        "returnDate": date,
        "options": [
            {
                "airline": airline_list[index % len(airline_list)] if index < len(airline_list) else "Various Airlines",
                "flightNumber": f"{'SQ' if 'Singapore' in airline_list[index % len(airline_list)] else 'MH' if 'Malaysia' in airline_list[index % len(airline_list)] else 'AI'} {100 + index}",
                "duration": f"{2 + index}h {15 * index}m",
                "stops": 0 if index == 0 else index % 2,
                "layover": "None" if index == 0 else f"{60 * index}m in Dubai",
                "cabinClasses": {
                    "economy": {"price": f"{currency_symbol}{base_price}", "available": True, "seatsLeft": f"{20 - index}"},
                    "premiumEconomy": {"price": f"{currency_symbol}{base_price * 2}", "available": True, "seatsLeft": f"{10 - index}"},
                    "business": {"price": f"{currency_symbol}{base_price * 3}", "available": index < 3, "seatsLeft": f"{5 - index}"}
                },
                "moneySavingTips": [
                    f"Book {segment_name} flight 2-3 months early",
                    "Consider weekday travel for better prices",
                    "Check airline website for direct bookings"
                ],
                "bookingLink": create_flight_search_url(departure, destination, date, date)
            }
        ]
    }

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
