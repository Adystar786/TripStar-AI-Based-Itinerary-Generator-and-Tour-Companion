// Global variables
let currentPlan = 'free';
let freeUsesRemaining = 3;
let currentSlide = 0;
let slideInterval;
let currentUser = null;

// Country and currency data
const countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", 
    "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", 
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", 
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", 
    "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", 
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", 
    "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", 
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", 
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", 
    "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", 
    "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", 
    "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", 
    "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", 
    "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
    "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", 
    "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", 
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", 
    "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
];

const currencies = [
    { code: "USD", name: "US Dollar", symbol: "$" },
    { code: "EUR", name: "Euro", symbol: "€" },
    { code: "GBP", name: "British Pound", symbol: "£" },
    { code: "JPY", name: "Japanese Yen", symbol: "¥" },
    { code: "CAD", name: "Canadian Dollar", symbol: "CA$" },
    { code: "AUD", name: "Australian Dollar", symbol: "A$" },
    { code: "CHF", name: "Swiss Franc", symbol: "CHF" },
    { code: "CNY", name: "Chinese Yuan", symbol: "¥" },
    { code: "INR", name: "Indian Rupee", symbol: "₹" },
    { code: "SGD", name: "Singapore Dollar", symbol: "S$" },
    { code: "NZD", name: "New Zealand Dollar", symbol: "NZ$" },
    { code: "KRW", name: "South Korean Won", symbol: "₩" },
    { code: "SEK", name: "Swedish Krona", symbol: "kr" },
    { code: "NOK", name: "Norwegian Krone", symbol: "kr" },
    { code: "DKK", name: "Danish Krone", symbol: "kr" },
    { code: "RUB", name: "Russian Ruble", symbol: "₽" },
    { code: "BRL", name: "Brazilian Real", symbol: "R$" },
    { code: "MXN", name: "Mexican Peso", symbol: "MX$" },
    { code: "TRY", name: "Turkish Lira", symbol: "₺" },
    { code: "ZAR", name: "South African Rand", symbol: "R" },
    { code: "AED", name: "UAE Dirham", symbol: "د.إ" },
    { code: "SAR", name: "Saudi Riyal", symbol: "﷼" },
    { code: "THB", name: "Thai Baht", symbol: "฿" },
    { code: "MYR", name: "Malaysian Ringgit", symbol: "RM" },
    { code: "IDR", name: "Indonesian Rupiah", symbol: "Rp" },
    { code: "PHP", name: "Philippine Peso", symbol: "₱" },
    { code: "VND", name: "Vietnamese Dong", symbol: "₫" },
    { code: "EGP", name: "Egyptian Pound", symbol: "E£" },
    { code: "PKR", name: "Pakistani Rupee", symbol: "₨" },
    { code: "BDT", name: "Bangladeshi Taka", symbol: "৳" }
];

// Enhanced country interests mapping
const countryInterests = {
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
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    
    // Add logout functionality
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
});

// Authentication check
function checkAuthentication() {
    fetch('/auth/check')
        .then(response => response.json())
        .then(data => {
            if (!data.authenticated) {
                // Redirect to welcome page if not authenticated
                window.location.href = '/';
                return;
            }
            
            // User is authenticated, continue with normal initialization
            currentUser = data.user;
            initializeApp(data.user);
        })
        .catch(error => {
            console.error('Auth check failed:', error);
            window.location.href = '/';
        });
}

// Initialize app with user data
function initializeApp(user) {
    console.log('User authenticated:', user);
    
    // Update UI with user info
    const userInfoElement = document.getElementById('user-info');
    if (userInfoElement) {
        userInfoElement.textContent = `Welcome, ${user.first_name} ${user.last_name}`;
    }
    
    // Set current plan from user data
    currentPlan = user.plan || 'free';
    
    // Update plan-specific features
    updatePlanFeatures(user.plan);
    
    // Initialize form elements
    initializeDestinationSearch();
    initializeCurrencySearch();
    initializeTravelerType();
    initializePlanSelection();
    loadUsageData();
    
    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('start-date').min = today;
    document.getElementById('end-date').min = today;
    
    // Add event listeners
    document.getElementById('start-date').addEventListener('change', updateEndDateMin);
    document.getElementById('itinerary-form').addEventListener('submit', handleFormSubmit);
    document.getElementById('regenerate-btn').addEventListener('click', resetForm);
    document.getElementById('download-btn').addEventListener('click', downloadPDF);
    document.getElementById('share-btn').addEventListener('click', shareViaWhatsApp);
    
    // Initialize date validation
    updateEndDateMin();
    
    // Set default values for better UX
    setDefaultValues();
}

// Update plan-specific features
function updatePlanFeatures(plan) {
    const proFeatures = document.querySelectorAll('.pro-feature');
    const freeUsesElement = document.getElementById('usage-counter');
    
    if (plan === 'free') {
        // Show free plan limitations
        proFeatures.forEach(feature => {
            feature.style.opacity = '0.6';
            feature.title = 'Upgrade to Pro to unlock this feature';
        });
        
        // Show usage counter
        if (freeUsesElement) {
            freeUsesElement.style.display = 'block';
        }
    } else {
        // Enable all features for pro users
        proFeatures.forEach(feature => {
            feature.style.opacity = '1';
            feature.title = '';
        });
        
        // Hide usage counter for pro users
        if (freeUsesElement) {
            freeUsesElement.style.display = 'none';
        }
    }
}

// Load usage data
async function loadUsageData() {
    try {
        const response = await fetch('/get-usage');
        const data = await response.json();
        freeUsesRemaining = data.free_uses_remaining;
        updateUsageCounter();
    } catch (error) {
        console.error('Failed to load usage data:', error);
    }
}

// Update usage counter
function updateUsageCounter() {
    const usageCounter = document.getElementById('usage-counter');
    const freeUsesSpan = document.getElementById('free-uses-remaining');
    
    if (currentPlan === 'free') {
        freeUsesSpan.textContent = freeUsesRemaining;
        usageCounter.style.display = 'block';
    } else {
        usageCounter.style.display = 'none';
    }
}

// Logout handler
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        window.location.href = '/auth/logout';
    }
}

function setDefaultValues() {
    // Set default traveler type
    const defaultTravelerBtn = document.querySelector('.traveler-type .option-btn[data-value="Solo"]');
    if (defaultTravelerBtn) {
        defaultTravelerBtn.click();
    }
    
    // Set default plan based on user's actual plan
    const defaultPlanValue = currentUser?.plan || 'free';
    const defaultPlanBtn = document.querySelector(`.traveler-type .option-btn[data-value="${defaultPlanValue}"]`);
    if (defaultPlanBtn) {
        defaultPlanBtn.click();
    }
    
    // Set default currency (USD)
    setTimeout(() => {
        const currencySearch = document.getElementById('currency-search');
        const currencyHidden = document.getElementById('currency');
        const currencySymbol = document.getElementById('currency-symbol');
        
        if (currencySearch && !currencySearch.value) {
            const usdCurrency = currencies.find(c => c.code === 'USD');
            if (usdCurrency) {
                currencySearch.value = `${usdCurrency.name} (${usdCurrency.code})`;
                currencyHidden.value = usdCurrency.code;
                currencySymbol.value = usdCurrency.symbol;
            }
        }
    }, 100);
}

// Searchable dropdown functionality
function initializeDestinationSearch() {
    const container = document.getElementById('destinations-container');
    
    // Add event listener for adding new destinations
    document.getElementById('add-destination').addEventListener('click', function() {
        addDestinationField();
    });
    
    // Initialize first destination field
    initializeDestinationField(container.children[0]);
}

function initializeDestinationField(destinationItem) {
    const searchInput = destinationItem.querySelector('.destination-search');
    const dropdown = destinationItem.querySelector('.dropdown-options');
    const hiddenInput = destinationItem.querySelector('.destination-value');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredCountries = countries.filter(country => 
            country.toLowerCase().includes(searchTerm)
        );
        
        updateDropdown(dropdown, filteredCountries, function(selectedCountry) {
            searchInput.value = selectedCountry;
            hiddenInput.value = selectedCountry;
            dropdown.style.display = 'none';
            updateInterests();
        });
    });
    
    searchInput.addEventListener('focus', function() {
        if (this.value === '') {
            updateDropdown(dropdown, countries.slice(0, 10), function(selectedCountry) {
                searchInput.value = selectedCountry;
                hiddenInput.value = selectedCountry;
                dropdown.style.display = 'none';
                updateInterests();
            });
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!destinationItem.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

function addDestinationField() {
    const container = document.getElementById('destinations-container');
    const destinationCount = container.children.length;
    
    if (destinationCount >= 5) {
        alert('Maximum 5 destinations allowed');
        return;
    }
    
    const newDestination = document.createElement('div');
    newDestination.className = 'destination-item';
    newDestination.innerHTML = `
        <div class="searchable-select">
            <input type="text" class="search-input destination-search" placeholder="Type to search countries...">
            <div class="dropdown-options" id="destination-options-${destinationCount}"></div>
        </div>
        <input type="hidden" class="destination-value">
        <button type="button" class="remove-destination">✕</button>
    `;
    
    container.appendChild(newDestination);
    
    // Initialize the new field
    initializeDestinationField(newDestination);
    
    // Add remove functionality
    newDestination.querySelector('.remove-destination').addEventListener('click', function() {
        if (container.children.length > 1) {
            container.removeChild(newDestination);
            updateInterests();
        }
    });
}

function initializeCurrencySearch() {
    const searchInput = document.getElementById('currency-search');
    const dropdown = document.getElementById('currency-options');
    const hiddenInput = document.getElementById('currency');
    const symbolInput = document.getElementById('currency-symbol');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredCurrencies = currencies.filter(currency => 
            currency.name.toLowerCase().includes(searchTerm) || 
            currency.code.toLowerCase().includes(searchTerm)
        );
        
        updateCurrencyDropdown(dropdown, filteredCurrencies, function(selectedCurrency) {
            searchInput.value = `${selectedCurrency.name} (${selectedCurrency.code})`;
            hiddenInput.value = selectedCurrency.code;
            symbolInput.value = selectedCurrency.symbol;
            dropdown.style.display = 'none';
        });
    });
    
    searchInput.addEventListener('focus', function() {
        if (this.value === '') {
            updateCurrencyDropdown(dropdown, currencies.slice(0, 10), function(selectedCurrency) {
                searchInput.value = `${selectedCurrency.name} (${selectedCurrency.code})`;
                hiddenInput.value = selectedCurrency.code;
                symbolInput.value = selectedCurrency.symbol;
                dropdown.style.display = 'none';
            });
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!searchInput.parentElement.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

function updateDropdown(dropdown, items, onSelect) {
    dropdown.innerHTML = '';
    
    if (items.length === 0) {
        dropdown.style.display = 'none';
        return;
    }
    
    items.forEach(item => {
        const option = document.createElement('div');
        option.className = 'dropdown-option';
        option.textContent = item;
        option.addEventListener('click', function() {
            onSelect(item);
        });
        dropdown.appendChild(option);
    });
    
    dropdown.style.display = 'block';
}

function updateCurrencyDropdown(dropdown, items, onSelect) {
    dropdown.innerHTML = '';
    
    if (items.length === 0) {
        dropdown.style.display = 'none';
        return;
    }
    
    items.forEach(item => {
        const option = document.createElement('div');
        option.className = 'dropdown-option';
        option.textContent = `${item.name} (${item.code}) - ${item.symbol}`;
        option.addEventListener('click', function() {
            onSelect(item);
        });
        dropdown.appendChild(option);
    });
    
    dropdown.style.display = 'block';
}

// Traveler type selection
function initializeTravelerType() {
    const travelerTypeBtns = document.querySelectorAll('.traveler-type .option-btn');
    
    travelerTypeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            travelerTypeBtns.forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
            document.getElementById('traveler-type').value = this.getAttribute('data-value');
        });
    });
}

// Plan selection
function initializePlanSelection() {
    const planBtns = document.querySelectorAll('.traveler-type .option-btn[data-value]');
    
    planBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const selectedPlan = this.getAttribute('data-value');
            
            // Update plan selection
            planBtns.forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
            document.getElementById('user-plan').value = selectedPlan;
            currentPlan = selectedPlan;
            
            console.log(`Selected plan: ${selectedPlan}`);
            
            // Show/hide budget friendly option
            const budgetSection = document.getElementById('budget-friendly-section');
            if (selectedPlan === 'pro') {
                budgetSection.style.display = 'block';
            } else {
                budgetSection.style.display = 'none';
                document.getElementById('budget-friendly').checked = false;
            }
            
            updateUsageCounter();
        });
    });
}

// Update interests based on selected destinations
async function updateInterests() {
    const interestsContainer = document.getElementById('interests-container');
    const destinations = Array.from(document.querySelectorAll('.destination-value'))
        .map(input => input.value)
        .filter(value => value);
    
    let availableInterests = new Set();
    
    // If we have destinations, try to get AI-suggested interests
    if (destinations.length > 0) {
        try {
            const aiInterests = await getAIInterests(destinations);
            aiInterests.forEach(interest => availableInterests.add(interest));
        } catch (error) {
            console.log('Using fallback interests:', error);
            // Fallback to static interests if AI fails
            destinations.forEach(destination => {
                const interests = countryInterests[destination] || countryInterests.default;
                interests.forEach(interest => availableInterests.add(interest));
            });
        }
    } else {
        // If no destinations selected, show default interests
        countryInterests.default.forEach(interest => availableInterests.add(interest));
    }
    
    interestsContainer.innerHTML = '';
    Array.from(availableInterests).forEach(interest => {
        const option = document.createElement('div');
        option.className = 'checkbox-option';
        option.innerHTML = `
            <input type="checkbox" value="${interest}">
            <span>${interest}</span>
        `;
        
        option.addEventListener('click', function() {
            this.classList.toggle('selected');
            const checkbox = this.querySelector('input');
            checkbox.checked = !checkbox.checked;
            updateSelectedInterests();
        });
        
        interestsContainer.appendChild(option);
    });
}

// Get AI-suggested interests based on destinations
async function getAIInterests(destinations) {
    try {
        const response = await fetch('/get-ai-interests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                destinations: destinations
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get AI interests');
        }
        
        const data = await response.json();
        return data.interests || [];
    } catch (error) {
        console.error('Error getting AI interests:', error);
        throw error;
    }
}

function updateSelectedInterests() {
    const selectedInterests = Array.from(document.querySelectorAll('.checkbox-option.selected'))
        .map(option => option.querySelector('input').value);
    
    document.getElementById('interests').value = selectedInterests.join(', ');
}

// Date validation
function updateEndDateMin() {
    const startDate = document.getElementById('start-date').value;
    if (startDate) {
        document.getElementById('end-date').min = startDate;
    }
}

// Form submission handler with authentication check
async function handleFormSubmit(e) {
    e.preventDefault();
    
    console.log('Form submission started...');
    
    // Check authentication first
    const authCheck = await fetch('/auth/check');
    const authData = await authCheck.json();
    
    if (!authData.authenticated) {
        alert('Please log in to generate itineraries');
        window.location.href = '/';
        return;
    }
    
    // Check free plan usage
    if (authData.user.plan === 'free') {
        const usageCheck = await fetch('/get-usage');
        const usageData = await usageCheck.json();
        
        if (usageData.free_uses_remaining <= 0) {
            alert('You have reached your daily limit of 3 free itineraries. Please upgrade to Pro for unlimited access.');
            return;
        }
    }
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Show loading section
    document.getElementById('form-section').style.display = 'none';
    document.getElementById('loading-section').style.display = 'block';
    document.getElementById('result-section').style.display = 'none';
    
    try {
        // Get form data and send to backend
        const formData = getFormData();
        console.log('Sending form data to backend:', formData);
        
        const response = await fetch('/generate-itinerary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || `Server error: ${response.status}`);
        }
        
        if (result.success) {
            // Update usage counter
            freeUsesRemaining = result.free_uses_remaining;
            updateUsageCounter();
            
            // Display the AI-generated itinerary
            displayItinerary(result.itinerary, formData);
        } else {
            throw new Error(result.error || 'Failed to generate itinerary');
        }
        
    } catch (error) {
        console.error('Error generating itinerary:', error);
        alert('Failed to generate itinerary: ' + error.message);
        // Show form again on error
        document.getElementById('loading-section').style.display = 'none';
        document.getElementById('form-section').style.display = 'block';
    }
}

// Form validation
function validateForm() {
    console.log('Starting form validation...');
    
    // Check user name
    const userName = document.getElementById('user-name');
    if (!userName.value.trim()) {
        alert('Please enter your name');
        userName.focus();
        return false;
    }
    
    // Check destinations
    const destinations = Array.from(document.querySelectorAll('.destination-value'))
        .map(input => input.value)
        .filter(value => value);
    
    if (destinations.length === 0) {
        alert('Please select at least one destination');
        return false;
    }
    
    // Check dates
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    if (!startDate.value) {
        alert('Please select a start date');
        startDate.focus();
        return false;
    }
    
    if (!endDate.value) {
        alert('Please select an end date');
        endDate.focus();
        return false;
    }
    
    // Check date validity
    const start = new Date(startDate.value);
    const end = new Date(endDate.value);
    
    if (end <= start) {
        alert('End date must be after start date');
        return false;
    }
    
    // Check traveler type
    const travelerType = document.getElementById('traveler-type');
    if (!travelerType.value) {
        alert('Please select a traveler type');
        return false;
    }
    
    // Check currency
    const currency = document.getElementById('currency');
    if (!currency.value) {
        alert('Please select a currency');
        return false;
    }
    
    // Check budget amount
    const budgetAmount = document.getElementById('budget-amount');
    if (!budgetAmount.value || budgetAmount.value <= 0) {
        alert('Please enter a valid budget amount');
        budgetAmount.focus();
        return false;
    }
    
    console.log('Form validation passed!');
    return true;
}

function getFormData() {
    const destinations = Array.from(document.querySelectorAll('.destination-value'))
        .map(input => input.value)
        .filter(value => value);
    
    const interests = Array.from(document.querySelectorAll('.checkbox-option.selected'))
        .map(option => option.querySelector('input').value);
    
    return {
        userName: document.getElementById('user-name').value,
        plan: document.getElementById('user-plan').value,
        budgetFriendly: document.getElementById('budget-friendly').checked,
        destinations: destinations,
        startDate: document.getElementById('start-date').value,
        endDate: document.getElementById('end-date').value,
        travelerType: document.getElementById('traveler-type').value,
        interests: interests.join(', '),
        currency: document.getElementById('currency').value,
        currencySymbol: document.getElementById('currency-symbol').value,
        budget: parseFloat(document.getElementById('budget-amount').value),
        notes: document.getElementById('notes').value
    };
}

function displayItinerary(itinerary, formData) {
    // Hide loading, show results
    document.getElementById('loading-section').style.display = 'none';
    document.getElementById('result-section').style.display = 'block';
    
    // Update result title
    document.getElementById('result-title').textContent = 
        `Your ${formData.destinations.join(' & ')} Itinerary`;
    
    // Clean the itinerary data before displaying
    const cleanedItinerary = cleanItineraryData(itinerary);
    
    // Generate itinerary HTML
    const itineraryHTML = createItineraryHTML(cleanedItinerary, formData);
    document.getElementById('itinerary-container').innerHTML = itineraryHTML;
    
    // Generate popular spots
    generatePopularSpots(cleanedItinerary.popularSpots || []);
    
    // Generate trip summary
    generateTripSummary(cleanedItinerary, formData);
    
    // Show/hide WhatsApp share button based on plan
    document.getElementById('share-btn').style.display = 
        currentPlan === 'pro' ? 'flex' : 'none';
}

// Helper function to clean itinerary data
function cleanItineraryData(itinerary) {
    const cleaned = JSON.parse(JSON.stringify(itinerary));
    
    if (cleaned.days) {
        cleaned.days.forEach(day => {
            if (day.description) {
                day.description = cleanText(day.description);
            }
            if (day.title) {
                day.title = cleanText(day.title);
            }
            if (day.tip) {
                day.tip = cleanText(day.tip);
            }
            if (day.activities) {
                day.activities = day.activities.map(activity => 
                    typeof activity === 'string' ? cleanText(activity) : activity
                );
            }
        });
    }
    
    if (cleaned.popularSpots) {
        cleaned.popularSpots.forEach(spot => {
            if (spot.name) spot.name = cleanText(spot.name);
            if (spot.description) spot.description = cleanText(spot.description);
        });
    }
    
    if (cleaned.summary) {
        cleaned.summary = cleanText(cleaned.summary);
    }
    
    return cleaned;
}

function createItineraryHTML(itinerary, formData) {
    let itineraryHTML = '';
    
    if (itinerary.days && Array.isArray(itinerary.days)) {
        itinerary.days.forEach(day => {
            const currentDate = new Date(formData.startDate);
            currentDate.setDate(currentDate.getDate() + (day.day - 1));
            
            itineraryHTML += `
                <div class="day-card">
                    <div class="day-header">
                        📅 Day ${day.day} - ${currentDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
                    </div>
                    <div class="day-content">
                        <h3>${day.title || `Day ${day.day} in ${formData.destinations[0]}`}</h3>
                        <p><strong>Overview:</strong> ${day.description || 'Explore and enjoy your journey.'}</p>
                        ${createActivitiesHTML(day.activities, formData.plan)}
                        <div class="pro-section">
                            <h4>💡 Travel Tip</h4>
                            <p>${day.tip || 'Enjoy your day and stay hydrated!'}</p>
                        </div>
                        ${formData.plan === 'pro' ? `
                            <div class="pro-details">
                                ${day.transportation ? `<p><strong>Transportation:</strong> ${day.transportation}</p>` : ''}
                                ${day.accommodation ? `<p><strong>Accommodation:</strong> ${day.accommodation}</p>` : ''}
                                ${day.dining ? `<p><strong>Dining:</strong> ${day.dining}</p>` : ''}
                                ${day.dailyBudget ? `<p><strong>Daily Budget:</strong> ${day.dailyBudget}</p>` : ''}
                            </div>
                        ` : ''}
                    </div>
                </div>
            `;
        });
    } else {
        itineraryHTML = '<p>No itinerary data available. Please try again.</p>';
    }
    
    return itineraryHTML;
}

function createActivitiesHTML(activities, plan) {
    if (!activities || !Array.isArray(activities)) {
        return '<p>No activities planned for this day.</p>';
    }
    
    if (plan === 'pro' && activities[0] && typeof activities[0] === 'object') {
        // Pro format with activity objects
        let activitiesHTML = '<div class="pro-activities"><h4>Daily Activities:</h4>';
        activities.forEach(activity => {
            activitiesHTML += `
                <div class="pro-activity-item">
                    <div class="activity-time">${activity.time || 'All day'}</div>
                    <div class="activity-desc">${activity.description || activity}</div>
                    ${activity.cost ? `<div class="activity-meta">💰 ${activity.cost}</div>` : ''}
                    ${activity.duration ? `<div class="activity-meta">⏱️ ${activity.duration}</div>` : ''}
                    ${activity.bookingLink && activity.bookingLink !== '#' ? 
                        `<a href="${activity.bookingLink}" class="booking-link-small" target="_blank">Book Now</a>` : ''}
                    ${activity.moneySavingTip ? `
                        <div class="money-saving-tip-small">
                            💡 ${activity.moneySavingTip}
                        </div>
                    ` : ''}
                </div>
            `;
        });
        activitiesHTML += '</div>';
        return activitiesHTML;
    } else {
        // Free format with string arrays
        let activitiesHTML = '<div class="activities-section"><h4>Daily Activities:</h4><ul class="activities-list">';
        activities.forEach(activity => {
            if (typeof activity === 'string') {
                activitiesHTML += `<li class="activity-item">${activity}</li>`;
            }
        });
        activitiesHTML += '</ul></div>';
        return activitiesHTML;
    }
}

function generatePopularSpots(popularSpots) {
    const spotsGrid = document.getElementById('spots-grid');
    spotsGrid.innerHTML = '';
    
    if (popularSpots && Array.isArray(popularSpots)) {
        popularSpots.forEach(spot => {
            const spotCard = document.createElement('div');
            spotCard.className = `spot-card ${currentPlan === 'pro' ? 'pro-spot' : ''}`;
            spotCard.innerHTML = `
                <h4>${spot.name}</h4>
                <p>${spot.description}</p>
                ${currentPlan === 'pro' && spot.bookingLink && spot.bookingLink !== '#' ? 
                    `<a href="${spot.bookingLink}" class="booking-link" target="_blank">Book Tickets</a>` : 
                    '<p style="color: #ffd700;">⭐ Upgrade to Pro for booking links</p>'}
                ${spot.moneySavingTip ? `
                    <div class="money-saving-tip">
                        💡 ${spot.moneySavingTip}
                    </div>
                ` : ''}
            `;
            spotsGrid.appendChild(spotCard);
        });
    } else {
        spotsGrid.innerHTML = '<p>No popular spots information available.</p>';
    }
}

function generateTripSummary(itinerary, formData) {
    const summaryText = document.getElementById('summary-text');
    
    if (itinerary.summary) {
        summaryText.textContent = itinerary.summary;
    } else {
        // Fallback summary
        const startDate = new Date(formData.startDate);
        const endDate = new Date(formData.endDate);
        const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
        
        summaryText.textContent = `This ${duration}-day ${formData.travelerType.toLowerCase()} trip to ${formData.destinations.join(' and ')} is perfectly crafted for your interests in ${formData.interests}. With a budget of ${formData.currencySymbol}${formData.budget.toLocaleString()}, you'll experience the best of local culture, cuisine, and attractions. ${formData.notes ? `Special notes: ${formData.notes}` : ''}`;
    }
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Get form data
    const userName = document.getElementById('user-name').value || 'Traveler';
    const destinations = Array.from(document.querySelectorAll('.destination-value'))
        .map(input => input.value)
        .filter(value => value);
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const travelerType = document.getElementById('traveler-type').value;
    const budget = document.getElementById('budget-amount').value;
    const currencySymbol = document.getElementById('currency-symbol').value;
    
    // Calculate duration
    const start = new Date(startDate);
    const end = new Date(endDate);
    const duration = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    
    // Set PDF properties
    doc.setProperties({
        title: `TripStar Itinerary - ${destinations.join(', ')}`,
        subject: 'AI-Generated Travel Itinerary',
        author: 'TripStar AI',
        keywords: 'travel, itinerary, ai, planning',
        creator: 'TripStar AI'
    });
    
    const pageWidth = doc.internal.pageSize.width;
    const pageHeight = doc.internal.pageSize.height;
    const margin = 20;
    const contentWidth = pageWidth - (2 * margin);
    
    let currentPage = 1;
    
    // ===== PAGE 1 - COVER PAGE =====
    let yPosition = 25;
    
    // Globe icon (simple circle)
    doc.setFillColor(70, 130, 180);
    doc.circle(23, 20, 3, 'F');
    
    // TripStar AI title
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(22);
    doc.setFont('helvetica', 'bold');
    doc.text('TripStar AI', 30, 23);
    
    // Subtitle
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(100, 100, 100);
    doc.text('Smart AI-Powered Itinerary Generator for Travel Professionals', margin, 32);
    
    yPosition = 50;
    
    // Main title with destination
    doc.setFontSize(20);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(0, 0, 0);
    doc.text(`Your ${destinations[0] || 'Destination'} Itinerary`, margin, yPosition);
    
    yPosition = 70;
    
    // Get all day cards
    const dayCards = document.querySelectorAll('.day-card');
    
    // ===== PROCESS EACH DAY =====
    dayCards.forEach((dayCard, dayIndex) => {
        // Check if we need a new page
        if (yPosition > 210) {
            addFooter(doc, currentPage);
            doc.addPage();
            currentPage++;
            yPosition = 25;
        }
        
        const dayHeader = cleanText(dayCard.querySelector('.day-header')?.textContent || `Day ${dayIndex + 1}`);
        const dayTitle = cleanText(dayCard.querySelector('h3')?.textContent || `Day ${dayIndex + 1} Activities`);
        const dayDesc = cleanText(dayCard.querySelector('p')?.textContent || 'Daily activities and exploration.');
        
        // Calendar icon (simple box)
        doc.setFillColor(240, 240, 240);
        doc.roundedRect(margin, yPosition - 3.5, 6, 6, 1, 1, 'F');
        doc.setFillColor(0, 0, 0);
        doc.setFontSize(8);
        doc.setFont('helvetica', 'bold');
        doc.text('D', margin + 2, yPosition + 1.5);
        
        // Day header
        doc.setFontSize(11);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(0, 0, 0);
        doc.text(dayHeader, margin + 9, yPosition + 1);
        yPosition += 10;
        
        // Day title
        doc.setFontSize(13);
        doc.setFont('helvetica', 'bold');
        const dayTitleLines = doc.splitTextToSize(dayTitle, contentWidth);
        dayTitleLines.forEach(line => {
            if (yPosition > 265) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            doc.text(line, margin, yPosition);
            yPosition += 6;
        });
        
        yPosition += 2;
        
        // Overview section
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        const overviewLabel = 'Overview: ';
        const overviewLabelWidth = doc.getTextWidth(overviewLabel);
        doc.text(overviewLabel, margin, yPosition);
        
        // Overview description
        doc.setFont('helvetica', 'normal');
        const overviewText = dayDesc.replace(/^Overview:\s*/i, '');
        const overviewLines = doc.splitTextToSize(overviewText, contentWidth);
        
        // First line continues after "Overview:"
        const firstLineWidth = contentWidth - overviewLabelWidth;
        const firstLinePart = doc.splitTextToSize(overviewLines[0], firstLineWidth);
        doc.text(firstLinePart[0], margin + overviewLabelWidth, yPosition);
        yPosition += 4.5;
        
        // Remaining overview text
        for (let i = 1; i < overviewLines.length; i++) {
            if (yPosition > 265) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            doc.text(overviewLines[i], margin, yPosition);
            yPosition += 4.5;
        }
        
        yPosition += 4;
        
        // Daily Activities header
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        doc.text('Daily Activities:', margin, yPosition);
        yPosition += 6;
        
        // Activities with checkmarks
        const activities = dayCard.querySelectorAll('.activity-item, .pro-activity-item');
        doc.setFontSize(9);
        doc.setFont('helvetica', 'normal');
        
        activities.forEach((activity) => {
            if (yPosition > 265) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            
            let activityText = cleanText(activity.textContent);
            if (activity.classList.contains('pro-activity-item')) {
                const time = cleanText(activity.querySelector('.activity-time')?.textContent || '');
                const desc = cleanText(activity.querySelector('.activity-desc')?.textContent || '');
                activityText = `${time} ${desc}`;
            }
            
            // Checkmark symbol
            doc.setFont('helvetica', 'normal');
            doc.text("✓", margin, yPosition);
            
            // Activity text with proper wrapping
            const activityLines = doc.splitTextToSize(activityText, contentWidth - 6);
            activityLines.forEach((line, lineIndex) => {
                if (yPosition > 265 && lineIndex > 0) {
                    addFooter(doc, currentPage);
                    doc.addPage();
                    currentPage++;
                    yPosition = 25;
                }
                doc.text(line, margin + 4, yPosition);
                if (lineIndex < activityLines.length - 1) {
                    yPosition += 4.5;
                }
            });
            yPosition += 6;
        });
        
        yPosition += 2;
        
        // Travel Tip section
        const dayTip = cleanText(dayCard.querySelector('.pro-section p')?.textContent || '');
        if (dayTip) {
            if (yPosition > 240) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            
            // Light bulb icon (simple circle)
            doc.setFillColor(255, 215, 0);
            doc.circle(margin + 3, yPosition + 1, 2.5, 'F');
            
            doc.setFillColor(0, 0, 0);
            doc.setFontSize(8);
            doc.setFont('helvetica', 'bold');
            doc.text('!', margin + 2.5, yPosition + 2.5);
            
            doc.setFontSize(10);
            doc.setFont('helvetica', 'bold');
            doc.setTextColor(0, 0, 0);
            doc.text('Travel Tip', margin + 8, yPosition + 2.5);
            
            yPosition += 8;
            
            doc.setFontSize(9);
            doc.setFont('helvetica', 'normal');
            const tipLines = doc.splitTextToSize(dayTip, contentWidth);
            tipLines.forEach(line => {
                if (yPosition > 265) {
                    addFooter(doc, currentPage);
                    doc.addPage();
                    currentPage++;
                    yPosition = 25;
                }
                doc.text(line, margin, yPosition);
                yPosition += 4.5;
            });
            
            yPosition += 8;
        } else {
            yPosition += 5;
        }
    });
    
    // ===== TRENDING DESTINATIONS SECTION =====
    if (yPosition > 170) {
        addFooter(doc, currentPage);
        doc.addPage();
        currentPage++;
        yPosition = 25;
    }
    
    // Fire icon (simple)
    doc.setFillColor(255, 100, 0);
    doc.circle(margin + 3, yPosition + 1.5, 2.5, 'F');
    
    doc.setFontSize(13);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(0, 0, 0);
    doc.text('Currently Trending in Your Destinations', margin + 9, yPosition + 2.5);
    yPosition += 12;
    
    // Trending spots
    const spotCards = document.querySelectorAll('.spot-card');
    spotCards.forEach((spotCard, index) => {
        if (yPosition > 240) {
            addFooter(doc, currentPage);
            doc.addPage();
            currentPage++;
            yPosition = 25;
        }
        
        const spotName = cleanText(spotCard.querySelector('h4')?.textContent || `Popular Spot ${index + 1}`);
        const spotDesc = cleanText(spotCard.querySelector('p')?.textContent || 'Explore this popular destination.');
        
        // Spot name
        doc.setFontSize(11);
        doc.setFont('helvetica', 'bold');
        doc.text(spotName, margin, yPosition);
        yPosition += 6;
        
        // Spot description
        doc.setFontSize(9);
        doc.setFont('helvetica', 'normal');
        const descLines = doc.splitTextToSize(spotDesc, contentWidth);
        descLines.forEach(line => {
            if (yPosition > 265) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            doc.text(line, margin, yPosition);
            yPosition += 4.5;
        });
        
        yPosition += 7;
    });
    
    // ===== TRIP SUMMARY SECTION =====
    if (yPosition > 220) {
        addFooter(doc, currentPage);
        doc.addPage();
        currentPage++;
        yPosition = 25;
    }
    
    // Clipboard icon (simple box)
    doc.setFillColor(200, 200, 200);
    doc.roundedRect(margin, yPosition - 2, 5, 6, 1, 1, 'F');
    doc.setFillColor(0, 0, 0);
    doc.setFontSize(7);
    doc.text('S', margin + 1.5, yPosition + 2);
    
    doc.setFontSize(13);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(0, 0, 0);
    doc.text('Trip Summary', margin + 8, yPosition + 2);
    yPosition += 10;
    
    // Summary text
    const summaryElement = document.getElementById('summary-text');
    const summaryText = cleanText(summaryElement?.textContent || 
        `This carefully curated ${duration}-day journey through ${destinations[0]} is designed for ${travelerType.toLowerCase()} travelers with a ${currencySymbol}${parseFloat(budget).toLocaleString()} budget. Experience an authentic blend of culture, cuisine, and adventure.`);
    
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    const summaryLines = doc.splitTextToSize(summaryText, contentWidth);
    summaryLines.forEach(line => {
        if (yPosition > 265) {
            addFooter(doc, currentPage);
            doc.addPage();
            currentPage++;
            yPosition = 25;
        }
        doc.text(line, margin, yPosition);
        yPosition += 4.5;
    });
    
    // Add footer to last page
    addFooter(doc, currentPage);
    
    // Save the PDF
    const filename = `tripstar-itinerary-${destinations[0]?.toLowerCase().replace(/\s+/g, '-') || 'trip'}.pdf`;
    doc.save(filename);
}

// Helper function to clean text
function cleanText(text) {
    if (!text) return '';
    return text
        .replace(/\s+/g, ' ')
        .replace(/Overview:\s*Overview:/gi, 'Overview:')
        .replace(/[^\x20-\x7E]/g, ' ')
        .trim();
}

// Helper function to add consistent footer
function addFooter(doc, pageNumber) {
    const pageWidth = doc.internal.pageSize.width;
    const pageHeight = doc.internal.pageSize.height;
    const margin = 20;
    const footerY = pageHeight - 10;
    
    doc.setFontSize(8);
    doc.setTextColor(120, 120, 120);
    doc.setFont('helvetica', 'normal');
    
    const year = new Date().getFullYear();
    
    // Left text
    doc.text(`© ${year} TripStar AI. All rights reserved.`, margin, footerY, { align: 'left' });
    
    // Center text
    doc.text('Smart AI-Powered Itinerary Generator for Travel Professionals', pageWidth / 2, footerY, { align: 'center' });
    
    // Right text
    doc.text(`Page ${pageNumber}`, pageWidth - margin, footerY, { align: 'right' });
}

// WhatsApp Share functionality
function shareViaWhatsApp() {
    if (currentPlan === 'free') {
        alert('WhatsApp sharing is available for Pro users only. Upgrade to share your itinerary.');
        return;
    }
    
    const itineraryText = `Check out my TripStar AI itinerary for ${Array.from(document.querySelectorAll('.destination-value')).map(input => input.value).join(', ')}!`;
    const encodedText = encodeURIComponent(itineraryText);
    const whatsappUrl = `https://wa.me/?text=${encodedText}`;
    
    window.open(whatsappUrl, '_blank');
}

// Reset form for new itinerary
function resetForm() {
    document.getElementById('result-section').style.display = 'none';
    document.getElementById('form-section').style.display = 'block';
    
    // Reset form fields
    document.getElementById('itinerary-form').reset();
    
    // Reset destination fields to just one
    const destinationsContainer = document.getElementById('destinations-container');
    while (destinationsContainer.children.length > 1) {
        destinationsContainer.removeChild(destinationsContainer.lastChild);
    }
    
    // Reset traveler type and plan selection
    document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
    document.querySelector('.traveler-type .option-btn[data-value="Solo"]')?.classList.add('selected');
    
    // Set plan based on user's actual plan
    const userPlan = currentUser?.plan || 'free';
    document.querySelector(`.traveler-type .option-btn[data-value="${userPlan}"]`)?.classList.add('selected');
    document.getElementById('traveler-type').value = 'Solo';
    document.getElementById('user-plan').value = userPlan;
    
    // Reset budget friendly section
    document.getElementById('budget-friendly-section').style.display = 'none';
    document.getElementById('budget-friendly').checked = false;
    
    // Update interests
    updateInterests();
    
    // Reload usage data
    loadUsageData();
    
    // Reset current plan
    currentPlan = userPlan;
    
    // Set default values again
    setDefaultValues();
}

// Plan selection function for pricing section
function selectPlan(plan) {
    const planBtns = document.querySelectorAll('.traveler-type .option-btn[data-value]');
    const targetBtn = Array.from(planBtns).find(btn => btn.getAttribute('data-value') === plan);
    
    if (targetBtn) {
        targetBtn.click();
    }
    
    // Scroll to form section
    document.getElementById('form-section')?.scrollIntoView({ behavior: 'smooth' });
}

// Make functions globally available for HTML onclick handlers
window.selectPlan = selectPlan;