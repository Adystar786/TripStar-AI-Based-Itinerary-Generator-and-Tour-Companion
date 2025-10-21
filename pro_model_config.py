import os
import json
import re
from dotenv import load_dotenv

print("Loading environment variables for Pro Model...")
load_dotenv()

try:
    from groq import Groq
    print("✓ Groq library imported successfully")
except ImportError:
    print("✗ Groq library not found!")
    Groq = None

class TripStarProModel:
    def __init__(self):
        """Initialize Groq AI model for Pro users"""
        print("\n" + "="*60)
        print("INITIALIZING TRIPSTAR AI PRO MODEL")
        print("="*60)
        
        if Groq is None:
            print("✗ Groq not installed.")
            self.client = None
            return
            
        try:
            # Get API key - try multiple sources
            self.api_key = os.getenv('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')
            print(f"API Key check: {'Found' if self.api_key else 'NOT FOUND'}")
            
            if not self.api_key:
                print("✗ GROQ_API_KEY not found!")
                self.client = None
                return
            
            # FIXED: Initialize Groq client without proxies parameter
            self.client = Groq(api_key=self.api_key)
            self.model_name = "llama-3.1-8b-instant"
            print(f"Selected PRO model: {self.model_name}")
            
            # Test connection
            try:
                test_response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": "Hi"}],
                    model=self.model_name,
                    max_tokens=5
                )
                print("✓ GROQ AI PRO MODEL READY!")
            except Exception as test_error:
                print(f"⚠️ API test warning: {test_error}")
                print("Will attempt to use client anyway...")
            
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"✗ PRO MODEL INITIALIZATION FAILED: {e}")
            self.client = None
    
    def generate_itinerary(self, user_data):
        """Generate comprehensive itinerary for Pro users"""
        if not self.client:
            print("⚠ No AI model available, using enhanced fallback")
            return self._create_pro_fallback_itinerary(user_data)
            
        try:
            prompt = self._create_pro_prompt(user_data)
            print(f"Generating PRO {user_data['days']}-day itinerary...")
            
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
                max_tokens=5500,
                top_p=1
            )
            
            response_text = response.choices[0].message.content.strip()
            parsed_data = self._parse_pro_response(response_text)
            
            if parsed_data and self._validate_pro_itinerary(parsed_data):
                print("✓ Successfully generated PRO itinerary!")
                return parsed_data
            else:
                print("⚠ Invalid PRO response, using enhanced fallback")
                return self._create_pro_fallback_itinerary(user_data)
            
        except Exception as e:
            print(f"✗ Error generating PRO itinerary: {e}")
            return self._create_pro_fallback_itinerary(user_data)
    
    def _create_pro_prompt(self, user_data):
        """Create comprehensive prompt for Pro users"""
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
        
        destinations_str = ', '.join(destinations)
        
        return f"""Create a comprehensive {days}-day PRO travel itinerary with:

TRIP DETAILS:
- Traveler: {user_name} ({traveler_type})
- Destinations: {destinations_str}
- Dates: {start_date} to {end_date}
- Budget: {currency_symbol}{budget}
- Interests: {interests}
- Special Notes: {notes}

RESPOND WITH THIS JSON STRUCTURE:
{{
  "days": [
    {{
      "day": 1,
      "location": "City Name",
      "title": "Day Title",
      "description": "Overview",
      "activities": [
        {{
          "time": "Morning (8:00-12:00)",
          "description": "Activity description",
          "duration": "2-3 hours",
          "cost": "{currency_symbol}50-100",
          "bookingLink": "https://www.viator.com",
          "moneySavingTip": "Tip here"
        }}
      ],
      "transportation": "Transport details",
      "accommodation": "Hotel recommendations",
      "dining": "Restaurant recommendations",
      "dailyBudget": "{currency_symbol}200-300",
      "tip": "Pro tip"
    }}
  ],
  "popularSpots": [
    {{
      "name": "Spot Name",
      "location": "City Name",
      "description": "Description",
      "bestTimeToVisit": "Morning",
      "entranceFee": "{currency_symbol}20",
      "bookingLink": "https://www.viator.com",
      "moneySavingTip": "Saving tip"
    }}
  ],
  "bookingResources": {{
    "flights": "https://www.skyscanner.com",
    "hotels": "https://www.booking.com",
    "localTours": "https://www.viator.com"
  }},
  "budgetBreakdown": {{
    "accommodation": "{currency_symbol}{int(budget * 0.4)}",
    "activities": "{currency_symbol}{int(budget * 0.3)}",
    "food": "{currency_symbol}{int(budget * 0.2)}",
    "transportation": "{currency_symbol}{int(budget * 0.1)}",
    "totalEstimated": "{currency_symbol}{budget}",
    "moneySavingStrategies": ["Strategy 1", "Strategy 2"]
  }},
  "summary": "Overview covering all destinations"
}}

Create exactly {days} days across destinations: {destinations_str}"""
    
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
        days_count = user_data.get('days', 3)
        budget = user_data.get('budget', 1000)
        currency = user_data.get('currency_symbol', '$')
        
        days = []
        for day in range(1, days_count + 1):
            days.append({
                "day": day,
                "location": destination_name,
                "title": f"Day {day} in {destination_name}",
                "description": f"Explore {destination_name}'s premium attractions",
                "activities": [
                    {
                        "time": "Morning (9:00-12:00)",
                        "description": "Luxury guided tour",
                        "duration": "3 hours",
                        "cost": f"{currency}80-120",
                        "bookingLink": "https://www.viator.com",
                        "moneySavingTip": "Book 7 days in advance for 20% discount"
                    }
                ],
                "transportation": "Private transfers included",
                "accommodation": f"5-star hotel in {destination_name}",
                "dining": "Fine dining experiences",
                "dailyBudget": f"{currency}250-400",
                "tip": "Book early for best rates"
            })
        
        return {
            "days": days,
            "popularSpots": [
                {
                    "name": f"{destination_name} Premium District",
                    "location": destination_name,
                    "description": "Experience the finest attractions",
                    "bestTimeToVisit": "Morning",
                    "entranceFee": f"{currency}25-50",
                    "bookingLink": "https://www.viator.com",
                    "moneySavingTip": "Book combo tickets online"
                }
            ],
            "bookingResources": {
                "flights": "https://www.skyscanner.com",
                "hotels": "https://www.booking.com",
                "localTours": "https://www.viator.com"
            },
            "budgetBreakdown": {
                "accommodation": f"{currency}{int(budget * 0.4)}",
                "activities": f"{currency}{int(budget * 0.3)}",
                "food": f"{currency}{int(budget * 0.2)}",
                "transportation": f"{currency}{int(budget * 0.1)}",
                "totalEstimated": f"{currency}{budget}",
                "moneySavingStrategies": [
                    "Book 2-3 months in advance",
                    "Use credit card travel benefits",
                    "Consider shoulder season travel"
                ]
            },
            "summary": f"This premium {days_count}-day itinerary offers luxury experiences in {destination_name}"
        }
