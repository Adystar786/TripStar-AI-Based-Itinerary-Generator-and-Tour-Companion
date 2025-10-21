import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Check if .env file exists
if os.path.exists('.env'):
    print("✓ .env file found")
else:
    print("✗ .env file NOT found! Create a .env file in your project root")

try:
    from groq import Groq
    print("✓ Groq library imported successfully")
except ImportError:
    print("✗ Groq library not found! Run: pip install groq")
    Groq = None

class TripStarAIModel:
    def __init__(self):
        """Initialize Groq AI model"""
        print("\n" + "="*60)
        print("INITIALIZING TRIPSTAR AI MODEL")
        print("="*60)
        
        if Groq is None:
            print("✗ Groq not installed. Install it with: pip install groq")
            self.client = None
            return
            
        try:
            # Get API key
            self.api_key = os.getenv('GROQ_API_KEY')
            print(f"API Key check: {'Found' if self.api_key else 'NOT FOUND'}")
            
            if not self.api_key:
                print("\n✗ GROQ_API_KEY not found in environment!")
                print("TO FIX THIS:")
                print("   1. Create a file named '.env' in your project folder")
                print("   2. Add this line to it:")
                print("      GROQ_API_KEY=your_actual_api_key_here")
                print("   3. Get your key from: https://console.groq.com/keys")
                print("")
                self.client = None
                return
            
            # Show partial key for verification (first 7 chars only)
            key_preview = self.api_key[:7] + "..." if len(self.api_key) > 7 else "too short!"
            print(f"API Key preview: {key_preview}")
            
            # Initialize Groq client - NO PROXIES PARAMETER
            print("Initializing Groq client...")
            self.client = Groq(api_key=self.api_key)
            
            # Use Llama 3.1 8B - faster for travel planning
            self.model_name = "llama-3.1-8b-instant"
            print(f"Selected model: {self.model_name}")
            
            # Test the connection
            print("Testing API connection...")
            test_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.model_name,
                max_tokens=10
            )
            
            print("✓ GROQ AI MODEL READY!")
            print(f"✓ Model: {self.model_name}")
            print(f"✓ Test response: {test_response.choices[0].message.content}")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n✗ INITIALIZATION FAILED!")
            print(f"✗ Error type: {type(e).__name__}")
            print(f"✗ Error message: {str(e)}")
            print("\nTROUBLESHOOTING:")
            print("   1. Check your API key is correct")
            print("   2. Verify internet connection")
            print("   3. Try: pip install --upgrade groq")
            print("   4. Get new key: https://console.groq.com/keys")
            print("="*60 + "\n")
            self.client = None
    
    def generate_itinerary(self, user_data):
        """Generate itinerary based on user plan"""
        user_plan = user_data.get('plan', 'free')
        
        print(f"Processing {user_plan.upper()} plan itinerary generation")
        
        if user_plan == 'pro':
            # Use Pro model for pro users
            try:
                print("Attempting to import Pro model...")
                from pro_model_config import TripStarProModel
                print("✓ Pro model imported successfully")
                pro_model = TripStarProModel()
                if pro_model.client:
                    print("Using Pro model for itinerary generation")
                    return pro_model.generate_itinerary(user_data)
                else:
                    print("⚠ Pro model client not available, using enhanced free version")
                    return self._create_pro_fallback_itinerary(user_data)
            except ImportError as e:
                print(f"✗ Pro model import error: {e}")
                print("Using enhanced free version as fallback")
                return self._create_pro_fallback_itinerary(user_data)
            except Exception as e:
                print(f"✗ Pro model initialization error: {e}")
                print("Using enhanced free version as fallback")
                return self._create_pro_fallback_itinerary(user_data)
        
        # Free plan - use existing logic
        print("Using Free model for itinerary generation")
        if not self.client:
            print("⚠ No AI model available, using fallback itinerary")
            return self._create_fallback_itinerary(user_data)
            
        try:
            prompt = self._create_prompt(user_data)
            print(f"Generating {user_data['days']}-day FREE itinerary with Groq AI...")
            
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
            
            print("AI Response received, parsing...")
            print(f"Response length: {len(response_text)} characters")
            
            # Parse the AI response
            parsed_data = self._parse_ai_response(response_text)
            
            if parsed_data and self._validate_itinerary(parsed_data):
                print("✓ Successfully generated FREE AI itinerary!")
                return parsed_data
            else:
                print("⚠ Invalid AI response structure, using fallback")
                return self._create_fallback_itinerary(user_data)
            
        except Exception as e:
            print(f"✗ Error generating FREE itinerary: {type(e).__name__}: {str(e)}")
            print("Falling back to template itinerary")
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
            print(f"⚠ JSON decode error at position {e.pos}: {e.msg}")
        
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
            print("⚠ Validation failed: Data is not a dictionary")
            return False
        
        required_keys = ['days', 'popularSpots', 'summary']
        if not all(key in data for key in required_keys):
            print(f"⚠ Validation failed: Missing keys. Found: {list(data.keys())}")
            return False
        
        if not isinstance(data['days'], list) or len(data['days']) == 0:
            print("⚠ Validation failed: Days is not a valid list")
            return False
        
        # Check first day structure
        first_day = data['days'][0]
        day_keys = ['day', 'title', 'description', 'activities', 'tip']
        if not all(key in first_day for key in day_keys):
            print(f"⚠ Validation failed: Day missing keys. Found: {list(first_day.keys())}")
            return False
        
        print("✓ Itinerary validation passed")
        return True
    
    def _create_prompt(self, user_data):
        """Create prompt for Groq AI"""
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
        
        destinations_str = ', '.join(destinations) if destinations else 'your destination'
        notes_section = f"\n- Special Notes: {notes}" if notes else ""
        
        return f"""Create a comprehensive {days}-day travel itinerary for:

TRIP DETAILS:
- Traveler: {user_name} ({traveler_type})
- Destinations: {destinations_str}
- Dates: {start_date} to {end_date}
- Budget: {currency_symbol}{budget}
- Interests: {interests}{notes_section}

Respond with ONLY this JSON structure (no markdown, no explanations):

{{
  "days": [
    {{
      "day": 1,
      "title": "Day Title",
      "description": "Day overview",
      "activities": [
        "Morning: Activity details",
        "Afternoon: Activity details",
        "Evening: Activity details"
      ],
      "tip": "Practical travel tip"
    }}
  ],
  "popularSpots": [
    {{
      "name": "Spot Name",
      "description": "Detailed description"
    }}
  ],
  "summary": "Trip overview"
}}

Create exactly {days} days with detailed activities."""
    
    def _create_fallback_itinerary(self, user_data):
        """Create fallback itinerary when AI fails"""
        days = user_data.get('days', 3)
        destinations = user_data.get('destinations', ['your destination'])
        destination_name = destinations[0] if destinations else "your destination"
        budget = user_data.get('budget', 1000)
        currency_symbol = user_data.get('currency_symbol', '$')
        
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
            "summary": f"This {days}-day journey through {destination_name} offers a blend of culture and exploration."
        }
        
        for day in range(1, days + 1):
            itinerary["days"].append({
                "day": day,
                "title": f"Day {day} in {destination_name}",
                "description": f"Explore {destination_name}'s attractions and culture.",
                "activities": [
                    "Morning: Cultural site visits",
                    "Afternoon: Local experiences",
                    "Evening: Dining and relaxation"
                ],
                "tip": "Wear comfortable shoes and stay hydrated."
            })
        
        return itinerary
    
    def _create_pro_fallback_itinerary(self, user_data):
        """Enhanced fallback for Pro users"""
        return self._create_fallback_itinerary(user_data)

    class Config:
        SECRET_KEY = 'your-secret-key-here'
        CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024import os
import json
import re
from dotenv import load_dotenv

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Check if .env file exists
if os.path.exists('.env'):
    print("✓ .env file found")
else:
    print("✗ .env file NOT found! Create a .env file in your project root")

try:
    from groq import Groq
    print("✓ Groq library imported successfully")
except ImportError:
    print("✗ Groq library not found! Run: pip install groq")
    Groq = None

class TripStarAIModel:
    def __init__(self):
        """Initialize Groq AI model"""
        print("\n" + "="*60)
        print("INITIALIZING TRIPSTAR AI MODEL")
        print("="*60)
        
        if Groq is None:
            print("✗ Groq not installed. Install it with: pip install groq")
            self.client = None
            return
            
        try:
            # Get API key
            self.api_key = os.getenv('GROQ_API_KEY')
            print(f"API Key check: {'Found' if self.api_key else 'NOT FOUND'}")
            
            if not self.api_key:
                print("\n✗ GROQ_API_KEY not found in environment!")
                print("TO FIX THIS:")
                print("   1. Create a file named '.env' in your project folder")
                print("   2. Add this line to it:")
                print("      GROQ_API_KEY=your_actual_api_key_here")
                print("   3. Get your key from: https://console.groq.com/keys")
                print("")
                self.client = None
                return
            
            # Show partial key for verification (first 7 chars only)
            key_preview = self.api_key[:7] + "..." if len(self.api_key) > 7 else "too short!"
            print(f"API Key preview: {key_preview}")
            
            # Initialize Groq client - NO PROXIES PARAMETER
            print("Initializing Groq client...")
            self.client = Groq(api_key=self.api_key)
            
            # Use Llama 3.1 8B - faster for travel planning
            self.model_name = "llama-3.1-8b-instant"
            print(f"Selected model: {self.model_name}")
            
            # Test the connection
            print("Testing API connection...")
            test_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.model_name,
                max_tokens=10
            )
            
            print("✓ GROQ AI MODEL READY!")
            print(f"✓ Model: {self.model_name}")
            print(f"✓ Test response: {test_response.choices[0].message.content}")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n✗ INITIALIZATION FAILED!")
            print(f"✗ Error type: {type(e).__name__}")
            print(f"✗ Error message: {str(e)}")
            print("\nTROUBLESHOOTING:")
            print("   1. Check your API key is correct")
            print("   2. Verify internet connection")
            print("   3. Try: pip install --upgrade groq")
            print("   4. Get new key: https://console.groq.com/keys")
            print("="*60 + "\n")
            self.client = None
    
    def generate_itinerary(self, user_data):
        """Generate itinerary based on user plan"""
        user_plan = user_data.get('plan', 'free')
        
        print(f"Processing {user_plan.upper()} plan itinerary generation")
        
        if user_plan == 'pro':
            # Use Pro model for pro users
            try:
                print("Attempting to import Pro model...")
                from pro_model_config import TripStarProModel
                print("✓ Pro model imported successfully")
                pro_model = TripStarProModel()
                if pro_model.client:
                    print("Using Pro model for itinerary generation")
                    return pro_model.generate_itinerary(user_data)
                else:
                    print("⚠ Pro model client not available, using enhanced free version")
                    return self._create_pro_fallback_itinerary(user_data)
            except ImportError as e:
                print(f"✗ Pro model import error: {e}")
                print("Using enhanced free version as fallback")
                return self._create_pro_fallback_itinerary(user_data)
            except Exception as e:
                print(f"✗ Pro model initialization error: {e}")
                print("Using enhanced free version as fallback")
                return self._create_pro_fallback_itinerary(user_data)
        
        # Free plan - use existing logic
        print("Using Free model for itinerary generation")
        if not self.client:
            print("⚠ No AI model available, using fallback itinerary")
            return self._create_fallback_itinerary(user_data)
            
        try:
            prompt = self._create_prompt(user_data)
            print(f"Generating {user_data['days']}-day FREE itinerary with Groq AI...")
            
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
            
            print("AI Response received, parsing...")
            print(f"Response length: {len(response_text)} characters")
            
            # Parse the AI response
            parsed_data = self._parse_ai_response(response_text)
            
            if parsed_data and self._validate_itinerary(parsed_data):
                print("✓ Successfully generated FREE AI itinerary!")
                return parsed_data
            else:
                print("⚠ Invalid AI response structure, using fallback")
                return self._create_fallback_itinerary(user_data)
            
        except Exception as e:
            print(f"✗ Error generating FREE itinerary: {type(e).__name__}: {str(e)}")
            print("Falling back to template itinerary")
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
            print(f"⚠ JSON decode error at position {e.pos}: {e.msg}")
        
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
            print("⚠ Validation failed: Data is not a dictionary")
            return False
        
        required_keys = ['days', 'popularSpots', 'summary']
        if not all(key in data for key in required_keys):
            print(f"⚠ Validation failed: Missing keys. Found: {list(data.keys())}")
            return False
        
        if not isinstance(data['days'], list) or len(data['days']) == 0:
            print("⚠ Validation failed: Days is not a valid list")
            return False
        
        # Check first day structure
        first_day = data['days'][0]
        day_keys = ['day', 'title', 'description', 'activities', 'tip']
        if not all(key in first_day for key in day_keys):
            print(f"⚠ Validation failed: Day missing keys. Found: {list(first_day.keys())}")
            return False
        
        print("✓ Itinerary validation passed")
        return True
    
    def _create_prompt(self, user_data):
        """Create prompt for Groq AI"""
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
        
        destinations_str = ', '.join(destinations) if destinations else 'your destination'
        notes_section = f"\n- Special Notes: {notes}" if notes else ""
        
        return f"""Create a comprehensive {days}-day travel itinerary for:

TRIP DETAILS:
- Traveler: {user_name} ({traveler_type})
- Destinations: {destinations_str}
- Dates: {start_date} to {end_date}
- Budget: {currency_symbol}{budget}
- Interests: {interests}{notes_section}

Respond with ONLY this JSON structure (no markdown, no explanations):

{{
  "days": [
    {{
      "day": 1,
      "title": "Day Title",
      "description": "Day overview",
      "activities": [
        "Morning: Activity details",
        "Afternoon: Activity details",
        "Evening: Activity details"
      ],
      "tip": "Practical travel tip"
    }}
  ],
  "popularSpots": [
    {{
      "name": "Spot Name",
      "description": "Detailed description"
    }}
  ],
  "summary": "Trip overview"
}}

Create exactly {days} days with detailed activities."""
    
    def _create_fallback_itinerary(self, user_data):
        """Create fallback itinerary when AI fails"""
        days = user_data.get('days', 3)
        destinations = user_data.get('destinations', ['your destination'])
        destination_name = destinations[0] if destinations else "your destination"
        budget = user_data.get('budget', 1000)
        currency_symbol = user_data.get('currency_symbol', '$')
        
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
            "summary": f"This {days}-day journey through {destination_name} offers a blend of culture and exploration."
        }
        
        for day in range(1, days + 1):
            itinerary["days"].append({
                "day": day,
                "title": f"Day {day} in {destination_name}",
                "description": f"Explore {destination_name}'s attractions and culture.",
                "activities": [
                    "Morning: Cultural site visits",
                    "Afternoon: Local experiences",
                    "Evening: Dining and relaxation"
                ],
                "tip": "Wear comfortable shoes and stay hydrated."
            })
        
        return itinerary
    
    def _create_pro_fallback_itinerary(self, user_data):
        """Enhanced fallback for Pro users"""
        return self._create_fallback_itinerary(user_data)

    class Config:
        SECRET_KEY = 'your-secret-key-here'
        CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024
