import os
import json
import re
from dotenv import load_dotenv

print("🔍 Loading environment variables for Pro Model...")
load_dotenv()

try:
    from groq import Groq
    print("✅ Groq library imported successfully")
except ImportError:
    print("❌ Groq library not found!")
    Groq = None

class TripStarProModel:
    def __init__(self):
        """Initialize Groq AI model for Pro users"""
        print("\n" + "="*60)
        print("🚀 INITIALIZING TRIPSTAR AI PRO MODEL")
        print("="*60)
        
        if Groq is None:
            print("❌ Groq not installed.")
            self.client = None
            return
            
        try:
            self.api_key = os.getenv('GROQ_API_KEY')
            print(f"🔑 API Key check: {'Found' if self.api_key else 'NOT FOUND'}")
            
            if not self.api_key:
                print("❌ GROQ_API_KEY not found!")
                self.client = None
                return
            
            # Initialize Groq client
            self.client = Groq(api_key=self.api_key)
            self.model_name = "llama-3.1-8b-instant"  # More powerful model for Pro
            print(f"🤖 Selected PRO model: {self.model_name}")
            
            print("✅ GROQ AI PRO MODEL READY!")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"❌ PRO MODEL INITIALIZATION FAILED: {e}")
            self.client = None
    
    def generate_itinerary(self, user_data):
        """Generate comprehensive itinerary for Pro users"""
        if not self.client:
            print("⚠️ No AI model available, using enhanced fallback")
            return self._create_pro_fallback_itinerary(user_data)
            
        try:
            prompt = self._create_pro_prompt(user_data)
            print(f"🎯 Generating PRO {user_data['days']}-day itinerary...")
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert travel planner for premium clients. Create highly detailed, 
                        comprehensive itineraries with booking links and budget optimization tips. 
                        Respond with ONLY valid JSON, no markdown."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model_name,
                temperature=0.7,
                max_tokens=5000,  # More tokens for detailed responses
                top_p=1
            )
            
            response_text = response.choices[0].message.content.strip()
            parsed_data = self._parse_pro_response(response_text)
            
            if parsed_data and self._validate_pro_itinerary(parsed_data):
                print("✅ Successfully generated PRO itinerary!")
                return parsed_data
            else:
                print("⚠️ Invalid PRO response, using enhanced fallback")
                return self._create_pro_fallback_itinerary(user_data)
            
        except Exception as e:
            print(f"❌ Error generating PRO itinerary: {e}")
            return self._create_pro_fallback_itinerary(user_data)
    
    # In pro_model_config.py, update the _create_pro_prompt method:

    def _create_pro_prompt(self, user_data):
        """Create comprehensive prompt for Pro users"""
        # Fix field name mismatches
        user_name = user_data.get('user_name', 'Traveler')
        traveler_type = user_data.get('traveler_type', 'Solo')
        destinations = user_data.get('destinations', [])
        start_date = user_data.get('start_date', '')
        end_date = user_data.get('end_date', '')
        budget = user_data.get('budget', 1000)
        currency_symbol = user_data.get('currency_symbol', '$')
        interests = user_data.get('interests', 'General sightseeing')
        notes = user_data.get('notes', '')
        days = user_data.get('days', 3)
        budget_friendly = user_data.get('budget_friendly', False)
        
        destinations_str = ', '.join(destinations)
        budget_friendly_text = " with strong focus on budget optimization and cost-saving tips" if budget_friendly else ""
        
        return f"""Create a comprehensive {days}-day PRO travel itinerary with:

            TRIP DETAILS:
            - Traveler: {user_name} ({traveler_type})
            - Destinations: {destinations_str}
            - Dates: {start_date} to {end_date}
            - Budget: {currency_symbol}{budget}{budget_friendly_text}
            - Interests: {interests}
            - Special Notes: {notes}

RESPOND WITH THIS JSON STRUCTURE:
{{
  "days": [
    {{
      "day": 1,
      "title": "Comprehensive Day Title",
      "description": "Detailed overview of the day's theme and highlights including cultural context, historical significance, architectural details, and local insights",
      "activities": [
        {{
          "time": "Morning (8:00-12:00)",
          "description": "Detailed activity description with historical context, cultural significance, and practical information",
          "duration": "2-3 hours",
          "cost": "Budget estimate",
          "bookingLink": "https://example.com/book-activity",
          "moneySavingTip": "Cost-saving tip for this activity"
        }}
      ],
      "transportation": "Detailed transport options with costs, historical context of transit systems, and local travel insights",
      "accommodation": "Hotel/lodging recommendations with booking links, architectural significance, and neighborhood context",
      "dining": "Restaurant recommendations with price ranges, culinary history, and cultural dining traditions",
      "dailyBudget": "Budget breakdown for the day",
      "tip": "Single comprehensive pro tip combining practical advice with cultural insights"
    }}
  ],
  "popularSpots": [
    {{
      "name": "Spot Name",
      "description": "Comprehensive description including historical context, architectural significance, cultural importance, visitor experience details, and local legends",
      "bestTimeToVisit": "Ideal timing with cultural and practical reasoning",
      "entranceFee": "Cost information with value context",
      "bookingLink": "https://example.com/book-tickets",
      "moneySavingTip": "How to save money here while maintaining experience quality"
    }}
  ],
  "bookingResources": {{
    "flights": "https://skyscanner.com/search-flights",
    "hotels": "https://booking.com/search-hotels",
    "localTours": "https://viator.com/local-tours",
    "transport": "https://rome2rio.com/transport-options",
    "travelInsurance": "https://worldnomads.com/travel-insurance"
  }},
  "budgetBreakdown": {{
    "accommodation": "Cost estimate with luxury/mid-range/budget options",
    "activities": "Cost estimate with premium/standard choices", 
    "food": "Cost estimate with fine dining/local cuisine options",
    "transportation": "Cost estimate with private/public transport choices",
    "miscellaneous": "Cost estimate for souvenirs and unexpected expenses",
    "totalEstimated": "Total cost analysis",
    "moneySavingStrategies": ["Comprehensive strategy 1", "Detailed strategy 2"]
  }},
  "summary": "Comprehensive 4-5 paragraph trip overview with cultural context, historical background, practical advice, and personalized recommendations based on traveler profile"
}}

REQUIREMENTS:
- Include REAL booking links for major activities (Skyscanner, Booking.com, Viator, etc.)
- Provide detailed cost breakdowns with context
- Add comprehensive money-saving tips for each major expense
- Include transportation details with historical and cultural context
- Suggest specific hotels/restaurants with architectural and culinary background
- Provide only ONE 'tip' per day (not 'proTips' array)
- Make descriptions extremely detailed with historical, cultural, and architectural context
- Focus on comprehensive location explanations and cultural significance"""
    
    def _parse_pro_response(self, response_text):
        """Parse Pro AI response"""
        response_text = re.sub(r'```json\s*', '', response_text)
        response_text = re.sub(r'```\s*', '', response_text)
        response_text = response_text.strip()
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return None
    
    def _validate_pro_itinerary(self, data):
        """Validate Pro itinerary structure"""
        required_keys = ['days', 'popularSpots', 'bookingResources', 'budgetBreakdown', 'summary']
        return all(key in data for key in required_keys)
    
    def _create_pro_fallback_itinerary(self, user_data):
        """Enhanced fallback for Pro users"""
        destinations = user_data.get('destinations', ['your destination'])
        destination_name = destinations[0] if destinations else "your destination"
        
        return {
            "days": self._create_pro_days(user_data, destination_name),
            "popularSpots": self._create_pro_spots(destination_name),
            "bookingResources": {
                "flights": "https://www.skyscanner.com",
                "hotels": "https://www.booking.com",
                "localTours": "https://www.viator.com",
                "transport": "https://www.rome2rio.com",
                "travelInsurance": "https://www.worldnomads.com"
            },
            "budgetBreakdown": {
                "accommodation": f"{user_data['currency_symbol']}{int(user_data['budget']) * 0.4}",
                "activities": f"{user_data['currency_symbol']}{int(user_data['budget']) * 0.3}",
                "food": f"{user_data['currency_symbol']}{int(user_data['budget']) * 0.2}",
                "transportation": f"{user_data['currency_symbol']}{int(user_data['budget']) * 0.1}",
                "totalEstimated": user_data['currency_symbol'] + str(user_data['budget']),
                "moneySavingStrategies": [
                    "Book flights 6-8 weeks in advance for optimal pricing while considering seasonal cultural events",
                    "Utilize local transportation systems to experience daily life while saving 60-70% compared to private transfers",
                    "Discover authentic local restaurants in residential neighborhoods for both cultural immersion and significant cost savings",
                    "Research free cultural events, museum discount days, and local festival schedules for budget-friendly entertainment",
                    "Travel during shoulder seasons to experience ideal weather conditions while avoiding peak pricing periods"
                ]
            },
            "summary": f"This premium {user_data['days']}-day itinerary through {destination_name} offers an unparalleled travel experience meticulously crafted for {user_data['traveler_type'].lower()} travelers. With a carefully optimized budget of {user_data['currency_symbol']}{user_data['budget']}, you'll enjoy luxury accommodations with historical significance, exclusive activities providing deep cultural immersion, and personalized service enhancing your understanding of local traditions. Our comprehensive planning includes direct booking links and sophisticated money-saving strategies that maximize your cultural experience while maintaining exceptional comfort and convenience. Each day is designed to provide not just sightseeing, but meaningful cultural engagement and historical context that transforms your journey into an educational and transformative experience."
        }
    
    def _create_pro_days(self, user_data, destination_name):
        """Create enhanced day itineraries for Pro users"""
        days = []
        for day in range(1, user_data['days'] + 1):
            if day == 1:
                days.append({
                    "day": day,
                    "title": f"Luxury Arrival and Cultural Introduction to {destination_name}",
                    "description": f"Begin your premium journey with seamless transfers to historically significant accommodations in the heart of {destination_name}. This day focuses on cultural orientation through carefully selected experiences that introduce you to the destination's architectural heritage, culinary traditions, and local lifestyle with expert historical context.",
                    "activities": [
                        {
                            "time": "Morning (9:00-12:00)",
                            "description": f"Private airport transfer to your 5-star hotel located in {destination_name}'s historic district, with guided commentary on significant architectural landmarks and urban development history during the journey",
                            "duration": "1 hour",
                            "cost": f"{user_data['currency_symbol']}50-80",
                            "bookingLink": "https://www.booking.com/transfer",
                            "moneySavingTip": "Book round-trip transfers for 15% discount and consider shared luxury transfers for additional savings"
                        },
                        {
                            "time": "Afternoon (14:00-17:00)",
                            "description": f"Exclusive guided tour of {destination_name}'s historic district with skip-the-line access to key landmarks, detailed architectural analysis, and insights into the cultural evolution that shaped the city's unique character",
                            "duration": "3 hours",
                            "cost": f"{user_data['currency_symbol']}75-120",
                            "bookingLink": "https://www.viator.com/exclusive-tours",
                            "moneySavingTip": "Book online 7 days in advance for 20% early bird discount and consider small group tours for personalized attention at better value"
                        }
                    ],
                    "transportation": "Private chauffeur service included with historical commentary. Comprehensive metro passes available for additional mobility and local cultural immersion experiences.",
                    "accommodation": f"Luxury Suite at {destination_name} Grand Hotel - a historically preserved building with modern amenities (from {user_data['currency_symbol']}200/night), featuring architectural significance from the colonial era",
                    "dining": f"Michelin-star restaurant experience showcasing fusion of traditional and contemporary culinary techniques ({user_data['currency_symbol']}80-150 per person), with sommelier-curated local wine pairings",
                    "dailyBudget": f"{user_data['currency_symbol']}300-450",
                    "tip": "Request early check-in when booking directly with heritage hotels for better room assignments, and download local ride-sharing apps that offer premium services at competitive prices for additional transport flexibility throughout your stay."
                })
            else:
                days.append({
                    "day": day,
                    "title": f"Premium Cultural Experience Day {day} in {destination_name}",
                    "description": f"Customized premium activities based on your interests in {destination_name}, focusing on deep cultural immersion, historical understanding, and authentic local experiences with expert guidance and comprehensive context.",
                    "activities": [
                        {
                            "time": "Flexible timing based on optimal cultural engagement",
                            "description": f"Personalized activities curated around {destination_name}'s unique cultural offerings, including private museum tours with art historians, traditional craft workshops with master artisans, or culinary experiences with local chefs preserving heritage recipes",
                            "duration": "Custom 4-6 hour immersive experience",
                            "cost": f"Varies based on selection ({user_data['currency_symbol']}100-300)",
                            "bookingLink": "https://www.viator.com/custom-tours",
                            "moneySavingTip": "Bundle multiple premium experiences for package discounts of 15-20%, and consider weekday bookings for better availability and pricing"
                        }
                    ],
                    "transportation": "Private driver for comfort combined with strategic use of public transport for authentic local experiences and cultural observation opportunities",
                    "accommodation": "Continuing at luxury heritage property with daily cultural programming and concierge services specializing in unique local experiences",
                    "dining": "Curated dining experiences moving between Michelin-recognized establishments and hidden local gems with cultural significance and historical ambiance",
                    "dailyBudget": f"{user_data['currency_symbol']}250-400",
                    "tip": "Consult with your hotel's cultural concierge for last-minute local experiences and insider access to special events; many premium hotels have partnerships offering exclusive access to normally restricted cultural sites and activities."
                })
        return days
    
    def _create_pro_spots(self, destination_name):
        """Create enhanced popular spots for Pro users"""
        return [
            {
                "name": f"{destination_name} Cultural Heritage District",
                "description": f"The historic heart of {destination_name} showcases centuries of architectural evolution, from colonial influences to contemporary designs. This carefully preserved district features UNESCO World Heritage sites, traditional markets operating for generations, and cultural institutions housing important historical artifacts. Visitors can trace the city's development through its buildings while experiencing living traditions maintained by local communities.",
                "bestTimeToVisit": "Early morning (8-10 AM) to experience local daily life rituals before tourist crowds arrive, or late afternoon (4-6 PM) for optimal photography light and to observe traditional evening cultural practices",
                "entranceFee": f"Varies by attraction (typically {destination_name} $10-25 for major sites), with comprehensive heritage passes offering 30% savings on multiple entries",
                "bookingLink": "https://www.viator.com/premium-tours",
                "moneySavingTip": "Purchase the city's cultural heritage pass for bundled access to multiple sites, and visit on first Sundays of the month when many museums offer free admission to support cultural accessibility"
            },
            {
                "name": "Local Artisan Communities and Traditional Craft Centers",
                "description": f"Authentic experiences with {destination_name}'s master artisans preserving traditional crafts that have been passed down through generations. These cultural hubs offer insights into local artistic traditions, from textile weaving with natural dyes to pottery techniques dating back centuries. Visitors can observe creation processes, understand cultural symbolism in designs, and support sustainable cultural preservation through responsible purchasing.",
                "bestTimeToVisit": "Weekday mornings (10 AM-12 PM) for the most active workshop periods and opportunities for meaningful interactions with artisans away from weekend tourist crowds",
                "entranceFee": "Typically free or donation-based, with workshop participation fees ranging $20-50 including materials and cultural explanations",
                "bookingLink": "https://www.airbnb.com/experiences",
                "moneySavingTip": "Book directly with artisan cooperatives rather than through tour operators to ensure more money supports the artists, and consider purchasing directly from workshop studios rather than tourist shops for authentic pieces at better prices"
            }
        ]