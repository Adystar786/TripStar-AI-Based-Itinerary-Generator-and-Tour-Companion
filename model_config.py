import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
print("🔍 Loading environment variables...")
load_dotenv()

# Check if .env file exists
if os.path.exists('.env'):
    print("✅ .env file found")
else:
    print("❌ .env file NOT found! Create a .env file in your project root")

try:
    from groq import Groq
    print("✅ Groq library imported successfully")
except ImportError:
    print("❌ Groq library not found! Run: pip install groq")
    Groq = None

class TripStarAIModel:
    def __init__(self):
        """Initialize Groq AI model"""
        print("\n" + "="*60)
        print("🚀 INITIALIZING TRIPSTAR AI MODEL")
        print("="*60)
        
        if Groq is None:
            print("❌ Groq not installed. Install it with: pip install groq")
            self.client = None
            return
            
        try:
            # Get API key
            self.api_key = os.getenv('GROQ_API_KEY')
            print(f"🔑 API Key check: {'Found' if self.api_key else 'NOT FOUND'}")
            
            if not self.api_key:
                print("\n❌ GROQ_API_KEY not found in environment!")
                print("📝 TO FIX THIS:")
                print("   1. Create a file named '.env' in your project folder")
                print("   2. Add this line to it:")
                print("      GROQ_API_KEY=your_actual_api_key_here")
                print("   3. Get your key from: https://console.groq.com/keys")
                print("")
                self.client = None
                return
            
            # Show partial key for verification (first 7 chars only)
            key_preview = self.api_key[:7] + "..." if len(self.api_key) > 7 else "too short!"
            print(f"🔑 API Key preview: {key_preview}")
            
            # Initialize Groq client
            print("🔄 Initializing Groq client...")
            self.client = Groq(api_key=self.api_key)
            
            # Use Llama 3.1 8B - faster for travel planning
            self.model_name = "llama-3.1-8b-instant"
            print(f"🤖 Selected model: {self.model_name}")
            
            # Test the connection
            print("🧪 Testing API connection...")
            test_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.model_name,
                max_tokens=10
            )
            
            print("✅ GROQ AI MODEL READY!")
            print(f"✅ Model: {self.model_name}")
            print(f"✅ Test response: {test_response.choices[0].message.content}")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n❌ INITIALIZATION FAILED!")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error message: {str(e)}")
            print("\n🔧 TROUBLESHOOTING:")
            print("   1. Check your API key is correct")
            print("   2. Verify internet connection")
            print("   3. Try: pip install --upgrade groq")
            print("   4. Get new key: https://console.groq.com/keys")
            print("="*60 + "\n")
            self.client = None
    
    def generate_itinerary(self, user_data):
        """Generate itinerary based on user plan"""
        user_plan = user_data.get('plan', 'free')
        
        print(f"🎯 Processing {user_plan.upper()} plan itinerary generation")
        print(f"📊 User data received: {user_data}")
        
        if user_plan == 'pro':
            # Use Pro model for pro users
            try:
                print("🔄 Attempting to import Pro model...")
                from pro_model_config import TripStarProModel
                print("✅ Pro model imported successfully")
                pro_model = TripStarProModel()
                if pro_model.client:  # Check if Pro model is properly initialized
                    print("🚀 Using Pro model for itinerary generation")
                    print(f"🔧 Pro model client status: {pro_model.client is not None}")
                    return pro_model.generate_itinerary(user_data)
                else:
                    print("⚠️ Pro model client not available, using enhanced free version")
                    print("🔧 Pro model client is None")
                    return self._create_pro_fallback_itinerary(user_data)
            except ImportError as e:
                print(f"❌ Pro model import error: {e}")
                print("🔄 Using enhanced free version as fallback")
                return self._create_pro_fallback_itinerary(user_data)
            except Exception as e:
                print(f"❌ Pro model initialization error: {e}")
                print("🔄 Using enhanced free version as fallback")
                return self._create_pro_fallback_itinerary(user_data)
        
        # Free plan - use existing logic
        print("🔄 Using Free model for itinerary generation")
        if not self.client:
            print("⚠️ No AI model available, using fallback itinerary")
            return self._create_fallback_itinerary(user_data)
            
        try:
            prompt = self._create_prompt(user_data)
            print(f"🎯 Generating {user_data['days']}-day FREE itinerary with Groq AI...")
            
            # Call Groq API
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional travel planner. You MUST respond with ONLY valid JSON, no markdown, no explanations, no code blocks. Just pure JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model_name,
                temperature=0.7,
                max_tokens=3000,
                top_p=1
            )
            
            response_text = response.choices[0].message.content.strip()
            
            print("📝 AI Response received, parsing...")
            print(f"📏 Response length: {len(response_text)} characters")
            
            # Parse the AI response
            parsed_data = self._parse_ai_response(response_text)
            
            if parsed_data and self._validate_itinerary(parsed_data):
                print("✅ Successfully generated FREE AI itinerary!")
                return parsed_data
            else:
                print("⚠️ Invalid AI response structure, using fallback")
                return self._create_fallback_itinerary(user_data)
            
        except Exception as e:
            print(f"❌ Error generating FREE itinerary: {type(e).__name__}: {str(e)}")
            print("🔄 Falling back to template itinerary")
            return self._create_fallback_itinerary(user_data)
    
    def _parse_ai_response(self, response_text):
        """Parse AI response with multiple strategies"""
        # Remove markdown code blocks if present
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        response_text = response_text.strip()
        
        # Strategy 1: Direct JSON parsing
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON decode error at position {e.pos}: {e.msg}")
        
        # Strategy 2: Find JSON object in text
        json_patterns = [
            r'\{[\s\S]*"days"[\s\S]*\}',
            r'\{[^}]*\{[^}]*\}[^}]*\}',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            if matches:
                for match in matches:
                    try:
                        json_str = match.strip()
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        continue
        
        return None
    
    def _validate_itinerary(self, data):
        """Validate itinerary structure"""
        if not isinstance(data, dict):
            print("⚠️ Validation failed: Data is not a dictionary")
            return False
        
        required_keys = ['days', 'popularSpots', 'summary']
        if not all(key in data for key in required_keys):
            print(f"⚠️ Validation failed: Missing keys. Found: {list(data.keys())}")
            return False
        
        if not isinstance(data['days'], list) or len(data['days']) == 0:
            print("⚠️ Validation failed: Days is not a valid list")
            return False
        
        # Check first day structure
        first_day = data['days'][0]
        day_keys = ['day', 'title', 'description', 'activities', 'tip']
        if not all(key in first_day for key in day_keys):
            print(f"⚠️ Validation failed: Day missing keys. Found: {list(first_day.keys())}")
            return False
        
        print("✅ Itinerary validation passed")
        return True
    
    def _create_prompt(self, user_data):
        """Create prompt for Groq AI with enhanced traveler type emphasis"""
        user_name = user_data.get('user_name', 'Traveler')
        traveler_type = user_data.get('traveler_type', 'Solo')
        destinations = user_data.get('destinations', [])
        destination_codes = user_data.get('destination_codes', [])
        start_date = user_data.get('start_date', '')
        end_date = user_data.get('end_date', '')
        budget = user_data.get('budget', 1000)
        currency_symbol = user_data.get('currency_symbol', '$')
        interests = user_data.get('interests', 'General sightseeing')
        notes = user_data.get('notes', '')
        days = user_data.get('days', 3)
        
        destinations_str = ', '.join(destinations) if destinations else 'your destination'
        codes_str = ', '.join(destination_codes) if destination_codes else ''
        notes_section = f"\n- Special Notes: {notes}" if notes else ""
        
        # Traveler type specific guidance
        traveler_guidance = {
            'Solo': 'Focus on social activities, safety, solo-friendly accommodations, and opportunities to meet other travelers.',
            'Couple': 'Emphasize romantic experiences, private accommodations, couple activities, and intimate dining.',
            'Family': 'Include child-friendly activities, family accommodations, educational experiences, and practical logistics for children.',
            'Group': 'Focus on group activities, larger accommodations, budget sharing options, and social dynamics.'
        }
        
        traveler_tips = traveler_guidance.get(traveler_type, 'Provide diverse experiences suitable for this traveler profile.')
        
        # Calculate days per destination for multiple destinations
        if len(destinations) > 1:
            days_per_dest = days // len(destinations)
            remaining_days = days % len(destinations)
            distribution = f"\nDistribute approximately {days_per_dest} days per destination"
            if remaining_days > 0:
                distribution += f" (with {remaining_days} extra day(s) for travel between destinations)"
        else:
            distribution = ""
        
        return f"""Create a comprehensive {days}-day travel itinerary for:

    TRIP DETAILS:
    - Traveler: {user_name} ({traveler_type})
    - Destinations: {destinations_str} ({codes_str})
    - Dates: {start_date} to {end_date}
    - Budget: {currency_symbol}{budget}
    - Interests: {interests}{notes_section}{distribution}

    CRITICAL TRAVELER-SPECIFIC REQUIREMENTS:
    - This itinerary is for a {traveler_type} traveler
    - {traveler_tips}
    - All activities, accommodations, and recommendations MUST be suitable for {traveler_type.lower()} travel
    - Consider the specific needs, preferences, and dynamics of {traveler_type.lower()} travel

    IMPORTANT - MULTIPLE DESTINATION ROUTING:
    {f"This is a MULTI-CITY trip visiting: {destinations_str}. Create itinerary that covers ALL destinations properly." if len(destinations) > 1 else ""}
    {f"Allocate days across all {len(destinations)} destinations. Include travel days between cities." if len(destinations) > 1 else ""}

    Provide detailed descriptions of locations, cultural context, historical significance, and practical information. 

    Respond with ONLY this JSON structure (no markdown, no explanations):

    {{
    "days": [
        {{
        "day": 1,
        "location": "{destinations[0] if destinations else 'Destination'}",
        "title": "Day Title",
        "description": "Comprehensive overview including which city you're in, cultural context, and activities. SPECIFICALLY TAILORED FOR {traveler_type.upper()} TRAVEL.",
        "activities": [
            "Morning: Specific activity with timing and location - SUITABLE FOR {traveler_type}",
            "Afternoon: Specific activity - SUITABLE FOR {traveler_type}",
            "Evening: Specific activity - SUITABLE FOR {traveler_type}"
        ],
        "tip": "Practical travel tip SPECIFICALLY FOR {traveler_type} travelers"
        }}
    ],
    "popularSpots": [
        {{
        "name": "Spot Name",
        "location": "City Name",
        "description": "Detailed description - HIGHLIGHT WHY THIS IS GOOD FOR {traveler_type}"
        }}
    ],
    "summary": "Comprehensive trip overview covering ALL destinations and SPECIFICALLY MENTIONING how it's tailored for {traveler_type} travel"
    }}

    REQUIREMENTS:
    - Create exactly {days} days covering ALL destinations: {destinations_str}
    - Clearly indicate which city each day is in
    - Include travel days between destinations if multiple cities
    - Include 4-6 popular spots across ALL destinations
    - Make activities specific to each destination AND suitable for {traveler_type}
    - ALL recommendations must consider {traveler_type} traveler needs
    - Stay within {currency_symbol}{budget} budget
    - Focus on {interests}
    - Make descriptions informative and engaging
    - HIGHLIGHT in descriptions why each activity is good for {traveler_type} travelers"""
    
    def _create_fallback_itinerary(self, user_data):
        """Create a realistic fallback itinerary when AI fails"""
        days = user_data.get('days', 3)
        destinations = user_data.get('destinations', ['your destination'])
        traveler_type = user_data.get('traveler_type', 'Solo')
        budget = user_data.get('budget', 1000)
        currency_symbol = user_data.get('currency_symbol', '$')
        interests = user_data.get('interests', 'General sightseeing')
        
        destination_name = destinations[0] if destinations else "your destination"
        
        itinerary = {
            "days": [],
            "popularSpots": [
                {
                    "name": f"{destination_name} Historic Center",
                    "description": f"Explore the cultural heart of {destination_name} with stunning architecture dating back centuries. This area showcases the rich history and local atmosphere through its preserved buildings, traditional markets, and vibrant street life. Visitors can immerse themselves in the authentic culture while admiring the intricate architectural details that tell stories of the past."
                },
                {
                    "name": "Local Food Markets", 
                    "description": f"Experience authentic culinary traditions at {destination_name}'s bustling local markets. These vibrant hubs offer fresh local produce, traditional spices, and street food that reflects the region's culinary heritage. Engage with local vendors, learn about traditional cooking methods, and taste flavors that have been passed down through generations."
                },
                {
                    "name": "Scenic Viewpoints",
                    "description": f"Discover breathtaking panoramic views of {destination_name}'s most iconic landscapes. These carefully selected vantage points offer perfect opportunities for photography while providing insights into the region's geographical significance. Learn about the natural formations and urban development that shaped the area's unique skyline."
                },
                {
                    "name": "Cultural Museums",
                    "description": f"Deep dive into {destination_name}'s rich history and artistic heritage through carefully curated museum collections. These institutions preserve important artifacts, traditional arts, and historical documents that showcase the evolution of local culture. Each exhibit tells a story of the people, traditions, and events that shaped the destination."
                },
                {
                    "name": "Hidden Gems District",
                    "description": f"Explore off-the-beaten-path neighborhoods in {destination_name} that are cherished by locals. These areas offer authentic experiences away from tourist crowds, featuring unique architecture, family-owned businesses, and community traditions. Discover the real character of the destination through its lesser-known but culturally significant locations."
                }
            ],
            "summary": f"This carefully curated {days}-day journey through {destination_name} is designed for {traveler_type.lower()} travelers with a {currency_symbol}{budget} budget. Experience an authentic blend of iconic landmarks, local culture, and {interests.lower()}. Each day balances must-see attractions with genuine local experiences, providing comprehensive cultural context and practical travel insights to enhance your understanding and enjoyment of this remarkable destination."
        }
        
        # Generate day-by-day itinerary
        for day in range(1, days + 1):
            if day == 1:
                itinerary["days"].append({
                    "day": day,
                    "title": f"Welcome to {destination_name} - Cultural Immersion Begins",
                    "description": f"Your adventure begins with a comprehensive introduction to {destination_name}'s rich cultural heritage and vibrant atmosphere. Settle in and get your first taste of the destination's unique character through carefully selected experiences that showcase its history, architecture, and local traditions.",
                    "activities": [
                        f"Morning: Arrive in {destination_name}, check into accommodation strategically located near cultural landmarks, and freshen up while learning about the neighborhood's historical significance",
                        f"Afternoon: Orientation walk through the main historical area, visiting carefully preserved architectural sites, local markets showcasing traditional crafts, and authentic cafes serving regional specialties with cultural context",
                        f"Evening: Welcome dinner at a traditional restaurant featuring regional specialties, with explanations of culinary traditions and their cultural importance in {destination_name}'s heritage"
                    ],
                    "tip": "Take time to absorb the local atmosphere and observe daily life patterns. Exchange some local currency for initial expenses at reputable locations, and don't over-plan day one to allow for cultural adjustment and spontaneous discoveries."
                })
            elif day == days:
                itinerary["days"].append({
                    "day": day,
                    "title": "Final Cultural Moments and Departure Preparation",
                    "description": "Make the most of your last hours with final explorations of culturally significant sites and heartfelt goodbyes to the locations that have become familiar. This day focuses on consolidating your cultural understanding while preparing for departure.",
                    "activities": [
                        "Morning: Last-minute souvenir shopping at local artisan markets with opportunities to learn about traditional crafting techniques and support local artisans preserving cultural heritage",
                        "Afternoon: Revisit your favorite culturally significant spot or discover one last hidden gem with enhanced appreciation based on your accumulated knowledge of the destination's history and traditions",
                        "Evening: Airport transfer with time to reflect on the cultural insights gained and wonderful memories to cherish, incorporating local farewell traditions"
                    ],
                    "tip": "Pack main luggage the night before to allow time for final cultural observations. Keep important documents and cultural souvenirs accessible. Arrive 3 hours early for international flights to accommodate any local travel considerations."
                })
            else:
                themes = [
                    ("Cultural Immersion Deep Dive", "exploring museums with significant historical collections, visiting carefully preserved heritage sites, and understanding architectural evolution"),
                    ("Natural Wonders Exploration", "discovering national parks with unique ecosystems, understanding geographical formations, and learning about local conservation efforts"),
                    ("Local Life Authentic Experience", "engaging with neighborhood communities, understanding daily traditions, and participating in authentic cultural practices"),
                    ("Adventure & Activity with Context", "outdoor activities that showcase the region's natural beauty while providing historical context about the landscape's significance"),
                    ("Relaxation & Cultural Leisure", "experiencing local leisure traditions, understanding recreational culture, and visiting spaces important to community life")
                ]
                
                theme_index = (day - 2) % len(themes)
                theme_name, theme_desc = themes[theme_index]
                
                itinerary["days"].append({
                    "day": day,
                    "title": theme_name,
                    "description": f"Today focuses on {theme_desc}, providing deep cultural insights and authentic experiences that enhance your understanding of {destination_name}'s unique character and traditions.",
                    "activities": [
                        f"Morning: Guided exploration of {theme_desc.split(',')[0]} with expert insights into historical context, cultural significance, and local importance of each location visited",
                        "Afternoon: Hands-on local experience - whether a cooking class demonstrating traditional techniques, a workshop in local arts, or cultural activity that provides deep immersion in authentic practices",
                        "Evening: Free time to wander with enhanced cultural understanding, dine at recommended spots showcasing regional variations, or join optional activities that further deepen cultural appreciation"
                    ],
                    "tip": "Wear comfortable shoes suitable for cultural sites and bring a refillable water bottle to stay hydrated during explorations. Download offline maps with cultural landmarks marked, and carry a notebook to record cultural insights and observations throughout the day."
                })
        
        return itinerary

    def _create_pro_fallback_itinerary(self, user_data):
        """Enhanced fallback for Pro users when Pro model fails"""
        print("🔄 Creating enhanced PRO fallback itinerary")
        
        destinations = user_data.get('destinations', ['your destination'])
        traveler_type = user_data.get('traveler_type', 'Solo')
        budget = user_data.get('budget', 1000)
        currency_symbol = user_data.get('currency_symbol', '$')
        interests = user_data.get('interests', 'General sightseeing')
        days = user_data.get('days', 3)
        
        destination_name = destinations[0] if destinations else "your destination"
        
        # Create Pro-style itinerary structure
        itinerary = {
            "days": [],
            "popularSpots": [
                {
                    "name": f"{destination_name} Premium Cultural District",
                    "description": f"Experience the finest cultural attractions in {destination_name} with exclusive access and premium guided tours. This district showcases the most significant historical landmarks, architectural marvels, and cultural institutions that define the destination's heritage.",
                    "bestTimeToVisit": "Morning hours for optimal lighting and smaller crowds",
                    "entranceFee": f"{currency_symbol}25-50 for premium access",
                    "bookingLink": "https://www.viator.com/premium-tours",
                    "moneySavingTip": "Book combo tickets online in advance for 20% discount on multiple attractions"
                },
                {
                    "name": "Luxury Dining & Culinary Experiences",
                    "description": f"Indulge in {destination_name}'s finest culinary offerings with curated dining experiences at award-winning restaurants and hidden local gems known only to connoisseurs.",
                    "bestTimeToVisit": "Evening reservations for the full fine dining experience",
                    "entranceFee": f"{currency_symbol}80-150 per person",
                    "bookingLink": "https://www.opentable.com/fine-dining",
                    "moneySavingTip": "Opt for lunch menus at fine dining restaurants for the same quality at 40% lower prices"
                }
            ],
            "bookingResources": {
                "flights": "https://www.skyscanner.com",
                "hotels": "https://www.booking.com/luxury",
                "localTours": "https://www.viator.com/premium",
                "transport": "https://www.uber.com/premium",
                "travelInsurance": "https://www.worldnomads.com/premium"
            },
            "budgetBreakdown": {
                "accommodation": f"{currency_symbol}{int(budget) * 0.4} (Luxury hotels & boutique stays)",
                "activities": f"{currency_symbol}{int(budget) * 0.3} (Premium experiences & private tours)",
                "food": f"{currency_symbol}{int(budget) * 0.2} (Fine dining & culinary experiences)",
                "transportation": f"{currency_symbol}{int(budget) * 0.1} (Private transfers & premium transport)",
                "totalEstimated": f"{currency_symbol}{budget}",
                "moneySavingStrategies": [
                    "Book luxury accommodations 2-3 months in advance for early bird discounts up to 25%",
                    "Utilize premium credit card travel benefits for airport lounge access and travel insurance",
                    "Consider shoulder season travel for luxury experiences at more accessible prices",
                    "Book private guides for small groups to split costs while maintaining exclusive access"
                ]
            },
            "summary": f"This premium {days}-day itinerary through {destination_name} offers an exclusive travel experience designed specifically for {traveler_type.lower()} travelers seeking luxury and depth. With a carefully curated budget of {currency_symbol}{budget}, you'll enjoy five-star accommodations, private guided tours with expert local insights, and culinary experiences that showcase the region's finest gastronomy. Each day is meticulously planned to provide not just sightseeing, but immersive cultural encounters and personalized service that transforms your journey into an unforgettable exploration of {destination_name}'s most exquisite offerings."
        }
        
        # Generate Pro-style days
        for day in range(1, days + 1):
            if day == 1:
                itinerary["days"].append({
                    "day": day,
                    "title": f"Luxury Arrival & Cultural Immersion in {destination_name}",
                    "description": f"Begin your premium journey with exclusive airport transfers and check-in at a luxury heritage property. This day focuses on cultural orientation through private guided experiences that introduce you to {destination_name}'s rich history and architectural significance with expert commentary and VIP access.",
                    "activities": [
                        {
                            "time": "Morning (9:00-12:00)",
                            "description": f"Private luxury airport transfer with guided commentary on {destination_name}'s history and architecture en route to your five-star accommodation in the historic district",
                            "duration": "1 hour",
                            "cost": f"{currency_symbol}60-100",
                            "bookingLink": "https://www.booking.com/luxury-transfers",
                            "moneySavingTip": "Book round-trip transfers for 15% discount and consider shared luxury transfers for additional savings"
                        },
                        {
                            "time": "Afternoon (14:00-17:00)",
                            "description": f"Exclusive guided tour of {destination_name}'s historic district with skip-the-line access to key landmarks, detailed architectural analysis, and insights into the cultural evolution that shaped the city's unique character",
                            "duration": "3 hours",
                            "cost": f"{currency_symbol}75-120",
                            "bookingLink": "https://www.viator.com/exclusive-tours",
                            "moneySavingTip": "Book online 7 days in advance for 20% early bird discount and consider small group tours for personalized attention at better value"
                        }
                    ],
                    "transportation": "Private chauffeur service included with historical commentary. Comprehensive metro passes available for additional mobility and local cultural immersion experiences.",
                    "accommodation": f"Luxury Suite at {destination_name} Grand Hotel - a historically preserved building with modern amenities (from {currency_symbol}200/night), featuring architectural significance from the colonial era",
                    "dining": f"Michelin-star restaurant experience showcasing fusion of traditional and contemporary culinary techniques ({currency_symbol}80-150 per person), with sommelier-curated local wine pairings",
                    "dailyBudget": f"{currency_symbol}300-450",
                    "tip": "Request early check-in when booking directly with heritage hotels for better room assignments, and download local ride-sharing apps that offer premium services at competitive prices for additional transport flexibility throughout your stay."
                })
            else:
                itinerary["days"].append({
                    "day": day,
                    "title": f"Premium Cultural Experience Day {day} in {destination_name}",
                    "description": f"Customized premium activities based on your interests in {destination_name}, focusing on deep cultural immersion, historical understanding, and authentic local experiences with expert guidance and comprehensive context.",
                    "activities": [
                        {
                            "time": "Flexible timing based on optimal cultural engagement",
                            "description": f"Personalized activities curated around {destination_name}'s unique cultural offerings, including private museum tours with art historians, traditional craft workshops with master artisans, or culinary experiences with local chefs preserving heritage recipes",
                            "duration": "Custom 4-6 hour immersive experience",
                            "cost": f"Varies based on selection ({currency_symbol}100-300)",
                            "bookingLink": "https://www.viator.com/custom-tours",
                            "moneySavingTip": "Bundle multiple premium experiences for package discounts of 15-20%, and consider weekday bookings for better availability and pricing"
                        }
                    ],
                    "transportation": "Private driver for comfort combined with strategic use of public transport for authentic local experiences and cultural observation opportunities",
                    "accommodation": "Continuing at luxury heritage property with daily cultural programming and concierge services specializing in unique local experiences",
                    "dining": "Curated dining experiences moving between Michelin-recognized establishments and hidden local gems with cultural significance and historical ambiance",
                    "dailyBudget": f"{currency_symbol}250-400",
                    "tip": "Consult with your hotel's cultural concierge for last-minute local experiences and insider access to special events; many premium hotels have partnerships offering exclusive access to normally restricted cultural sites and activities."
                })
        
        return itinerary
    
    class Config:
        SECRET_KEY = 'your-secret-key-here'
        CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size