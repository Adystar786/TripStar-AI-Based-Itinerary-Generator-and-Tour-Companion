// Global variables
let currentPlan = 'free';
let freeUsesRemaining = 3;
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

// Major airports with IATA codes
const majorAirports = [
    // USA
    { city: "New York", country: "USA", code: "JFK", name: "John F. Kennedy International" },
    { city: "New York", country: "USA", code: "LGA", name: "LaGuardia" },
    { city: "New York", country: "USA", code: "EWR", name: "Newark Liberty International" },
    { city: "Los Angeles", country: "USA", code: "LAX", name: "Los Angeles International" },
    { city: "Chicago", country: "USA", code: "ORD", name: "O'Hare International" },
    { city: "San Francisco", country: "USA", code: "SFO", name: "San Francisco International" },
    { city: "Miami", country: "USA", code: "MIA", name: "Miami International" },
    { city: "Boston", country: "USA", code: "BOS", name: "Logan International" },
    
    // Europe
    { city: "London", country: "UK", code: "LHR", name: "Heathrow" },
    { city: "London", country: "UK", code: "LGW", name: "Gatwick" },
    { city: "Paris", country: "France", code: "CDG", name: "Charles de Gaulle" },
    { city: "Paris", country: "France", code: "ORY", name: "Orly" },
    { city: "Frankfurt", country: "Germany", code: "FRA", name: "Frankfurt Airport" },
    { city: "Amsterdam", country: "Netherlands", code: "AMS", name: "Schiphol" },
    { city: "Madrid", country: "Spain", code: "MAD", name: "Adolfo Suárez Madrid-Barajas" },
    { city: "Barcelona", country: "Spain", code: "BCN", name: "Barcelona-El Prat" },
    { city: "Rome", country: "Italy", code: "FCO", name: "Leonardo da Vinci-Fiumicino" },
    { city: "Milan", country: "Italy", code: "MXP", name: "Malpensa" },
    
    // Middle East
    { city: "Dubai", country: "UAE", code: "DXB", name: "Dubai International" },
    { city: "Abu Dhabi", country: "UAE", code: "AUH", name: "Abu Dhabi International" },
    { city: "Doha", country: "Qatar", code: "DOH", name: "Hamad International" },
    { city: "Istanbul", country: "Turkey", code: "IST", name: "Istanbul Airport" },
    { city: "Tehran", country: "Iran", code: "IKA", name: "Imam Khomeini International" },
    { city: "Tehran", country: "Iran", code: "THR", name: "Mehrabad International" },
    
    // Asia
    { city: "Tokyo", country: "Japan", code: "NRT", name: "Narita International" },
    { city: "Tokyo", country: "Japan", code: "HND", name: "Haneda" },
    { city: "Seoul", country: "South Korea", code: "ICN", name: "Incheon International" },
    { city: "Beijing", country: "China", code: "PEK", name: "Beijing Capital International" },
    { city: "Shanghai", country: "China", code: "PVG", name: "Pudong International" },
    { city: "Hong Kong", country: "Hong Kong", code: "HKG", name: "Hong Kong International" },
    { city: "Singapore", country: "Singapore", code: "SIN", name: "Changi Airport" },
    { city: "Bangkok", country: "Thailand", code: "BKK", name: "Suvarnabhumi" },
    { city: "Kuala Lumpur", country: "Malaysia", code: "KUL", name: "Kuala Lumpur International" },
    { city: "Delhi", country: "India", code: "DEL", name: "Indira Gandhi International" },
    { city: "Mumbai", country: "India", code: "BOM", name: "Chhatrapati Shivaji Maharaj International" },
    { city: "Bangalore", country: "India", code: "BLR", name: "Kempegowda International" },
    { city: "Kabul", country: "Afghanistan", code: "KBL", name: "Hamid Karzai International" },
    
    // Australia & Oceania
    { city: "Sydney", country: "Australia", code: "SYD", name: "Kingsford Smith" },
    { city: "Melbourne", country: "Australia", code: "MEL", name: "Melbourne Airport" },
    { city: "Auckland", country: "New Zealand", code: "AKL", name: "Auckland Airport" },
    
    // Africa
    { city: "Johannesburg", country: "South Africa", code: "JNB", name: "O.R. Tambo International" },
    { city: "Cairo", country: "Egypt", code: "CAI", name: "Cairo International" },
    { city: "Nairobi", country: "Kenya", code: "NBO", name: "Jomo Kenyatta International" },
    
    // South America
    { city: "São Paulo", country: "Brazil", code: "GRU", name: "Guarulhos International" },
    { city: "Buenos Aires", country: "Argentina", code: "EZE", name: "Ministro Pistarini International" },
    { city: "Lima", country: "Peru", code: "LIM", name: "Jorge Chávez International" },
    
    // Canada
    { city: "Toronto", country: "Canada", code: "YYZ", name: "Pearson International" },
    { city: "Vancouver", country: "Canada", code: "YVR", name: "Vancouver International" },
    { city: "Montreal", country: "Canada", code: "YUL", name: "Montréal-Pierre Elliott Trudeau" }
];

// Enhanced country interests with city-specific details
const cityInterests = {
    "Tehran": ["Historical Palaces", "Persian Gardens", "Bazaar Shopping", "Mountain Hiking", "Museums", "Persian Cuisine", "Traditional Tea Houses", "Carpet Markets", "Islamic Architecture", "Mount Tochal"],
    "Kabul": ["Historical Sites", "Local Markets", "Mountain Views", "Afghan Cuisine", "Traditional Crafts", "Gardens", "Cultural Museums", "Local Life Experience"],
    "Paris": ["Eiffel Tower", "Louvre Museum", "Wine Tasting", "Gourmet Food", "Shopping", "Romantic Getaways", "Art Museums", "Seine River Cruise"],
    "London": ["British Museum", "Tower of London", "West End Shows", "Afternoon Tea", "Royal Palaces", "Markets", "Pub Culture", "Thames River"],
    // Add more cities as needed
};

// Enhanced country interests mapping
const countryInterests = {
    "France": ["Wine Tasting", "Art Museums", "Historical Sites", "Gourmet Food", "Shopping", "Romantic Getaways"],
    "Italy": ["Historical Sites", "Art Museums", "Wine Tasting", "Cooking Classes", "Beach Relaxation", "Shopping"],
    "Japan": ["Temples & Shrines", "Anime & Manga", "Sushi Making", "Hot Springs", "Cherry Blossoms", "Shopping"],
    "USA": ["National Parks", "Theme Parks", "Shopping", "Beach Activities", "City Tours", "Food Tours"],
    "Spain": ["Flamenco Shows", "Beach Relaxation", "Historical Sites", "Tapas Tours", "Shopping", "Nightlife"],
    "Thailand": ["Temples", "Beach Activities", "Elephant Sanctuaries", "Street Food", "Island Hopping", "Shopping"],
    "India": ["Historical Monuments", "Yoga & Meditation", "Spiritual Sites", "Local Markets", "Wildlife Safaris", "Food Tours"],
    "Australia": ["Beach Activities", "Wildlife Viewing", "Wine Tasting", "Outdoor Adventures", "City Tours"],
    "Greece": ["Historical Sites", "Island Hopping", "Beach Relaxation", "Greek Cuisine", "Sunset Views", "Shopping"],
    "Germany": ["Historical Sites", "Beer Tasting", "Castle Tours", "Christmas Markets", "City Tours", "Museums"],
    "default": ["Historical Sites", "Local Cuisine", "Shopping", "Nature & Parks", "Cultural Experiences", "Adventure Activities"]
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');
    checkAuthentication();
});

// Authentication check
function checkAuthentication() {
    fetch('/auth/check')
        .then(response => response.json())
        .then(data => {
            if (!data.authenticated) {
                window.location.href = '/';
                return;
            }
            
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
    console.log('Initializing app for user:', user);
    
    // Set current plan from user data
    currentPlan = user.plan || 'free';
    
    // Set hidden plan field
    const planField = document.getElementById('user-plan');
    if (planField) {
        planField.value = currentPlan;
    }
    
    // Update plan-specific features
    updatePlanFeatures(user.plan);
    
    // Initialize form elements
    initializeDepartureCitySearch();  
    initializeDestinationSearch();
    initializeCurrencySearch();
    initializeTravelerType();
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
    
    // Set default values
    setDefaultValues();
    
    console.log('App initialization complete');
}

// Update plan-specific features
function updatePlanFeatures(plan) {
    const budgetSection = document.getElementById('budget-friendly-section');
    const usageCounter = document.getElementById('usage-counter');
    
    if (plan === 'pro') {
        budgetSection.style.display = 'block';
        usageCounter.style.display = 'none';
    } else {
        budgetSection.style.display = 'none';
        usageCounter.style.display = 'block';
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
    const freeUsesSpan = document.getElementById('free-uses-display');
    if (freeUsesSpan && currentPlan === 'free') {
        freeUsesSpan.textContent = freeUsesRemaining;
    }
}

function setDefaultValues() {
    // Set default traveler type
    const defaultTravelerBtn = document.querySelector('.traveler-type .option-btn[data-value="Solo"]');
    if (defaultTravelerBtn) {
        defaultTravelerBtn.click();
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
    
    document.getElementById('add-destination').addEventListener('click', function() {
        addDestinationField();
    });
    
    initializeDestinationField(container.children[0]);
}

// Initialize departure city search
function initializeDepartureCitySearch() {
    const searchInput = document.getElementById('departure-city-search');
    const dropdown = document.getElementById('departure-city-options');
    const hiddenInput = document.getElementById('departure-city');
    const hiddenCodeInput = document.getElementById('departure-city-code');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredAirports = majorAirports.filter(airport => 
            airport.city.toLowerCase().includes(searchTerm) ||
            airport.code.toLowerCase().includes(searchTerm) ||
            airport.country.toLowerCase().includes(searchTerm) ||
            airport.name.toLowerCase().includes(searchTerm)
        );
        
        updateAirportDropdown(dropdown, filteredAirports, function(selectedAirport) {
            searchInput.value = `${selectedAirport.city}, ${selectedAirport.country} (${selectedAirport.code})`;
            hiddenInput.value = `${selectedAirport.city}, ${selectedAirport.country}`;
            hiddenCodeInput.value = selectedAirport.code;
            dropdown.style.display = 'none';
        });
    });
    
    searchInput.addEventListener('focus', function() {
        if (this.value === '') {
            const topAirports = majorAirports.slice(0, 10);
            updateAirportDropdown(dropdown, topAirports, function(selectedAirport) {
                searchInput.value = `${selectedAirport.city}, ${selectedAirport.country} (${selectedAirport.code})`;
                hiddenInput.value = `${selectedAirport.city}, ${selectedAirport.country}`;
                hiddenCodeInput.value = selectedAirport.code;
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

function updateAirportDropdown(dropdown, airports, onSelect) {
    dropdown.innerHTML = '';
    
    if (airports.length === 0) {
        dropdown.style.display = 'none';
        return;
    }
    
    airports.forEach(airport => {
        const option = document.createElement('div');
        option.className = 'dropdown-option';
        option.innerHTML = `
            <strong>${airport.city}, ${airport.country}</strong> 
            <span style="color: #666; font-size: 0.9em;">(${airport.code}) - ${airport.name}</span>
        `;
        option.addEventListener('click', function() {
            onSelect(airport);
        });
        dropdown.appendChild(option);
    });
    
    dropdown.style.display = 'block';
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
            <input type="text" class="search-input destination-search" 
                   placeholder="Type city or airport code...">
            <div class="dropdown-options" id="destination-options-${destinationCount}"></div>
        </div>
        <input type="hidden" class="destination-value">
        <input type="hidden" class="destination-code">
        <button type="button" class="remove-destination">✕</button>
    `;
    
    container.appendChild(newDestination);
    initializeDestinationField(newDestination);
    
    newDestination.querySelector('.remove-destination').addEventListener('click', function() {
        if (container.children.length > 1) {
            container.removeChild(newDestination);
            updateInterests();
        }
    });
}

function initializeDestinationField(destinationItem) {
    const searchInput = destinationItem.querySelector('.destination-search');
    const dropdown = destinationItem.querySelector('.dropdown-options');
    const hiddenInput = destinationItem.querySelector('.destination-value');
    const hiddenCodeInput = destinationItem.querySelector('.destination-code');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredAirports = majorAirports.filter(airport => 
            airport.city.toLowerCase().includes(searchTerm) ||
            airport.code.toLowerCase().includes(searchTerm) ||
            airport.country.toLowerCase().includes(searchTerm) ||
            airport.name.toLowerCase().includes(searchTerm)
        );
        
        updateAirportDropdown(dropdown, filteredAirports, function(selectedAirport) {
            searchInput.value = `${selectedAirport.city}, ${selectedAirport.country} (${selectedAirport.code})`;
            hiddenInput.value = `${selectedAirport.city}, ${selectedAirport.country}`;
            hiddenCodeInput.value = selectedAirport.code;
            dropdown.style.display = 'none';
            updateInterests(); // Refresh interests for all destinations
        });
    });
    
    searchInput.addEventListener('focus', function() {
        if (this.value === '') {
            const topAirports = majorAirports.slice(0, 10);
            updateAirportDropdown(dropdown, topAirports, function(selectedAirport) {
                searchInput.value = `${selectedAirport.city}, ${selectedAirport.country} (${selectedAirport.code})`;
                hiddenInput.value = `${selectedAirport.city}, ${selectedAirport.country}`;
                hiddenCodeInput.value = selectedAirport.code;
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

// Update interests based on selected destinations with SEPARATE interest groups
async function updateInterests() {
    const interestsContainer = document.getElementById('interests-container');
    const destinationItems = document.querySelectorAll('.destination-item');
    
    const destinations = Array.from(destinationItems)
        .map(item => ({
            name: item.querySelector('.destination-value').value.trim(),
            code: item.querySelector('.destination-code').value.trim()
        }))
        .filter(dest => dest.name && dest.code);
    
    console.log('Updating interests for destinations:', destinations);
    
    // Show skeleton loading state
    interestsContainer.innerHTML = '';
    interestsContainer.classList.remove('interests-loaded');
    
    // Create skeleton items
    for (let i = 0; i < 8; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-interest';
        skeleton.innerHTML = `
            <div class="skeleton-interest-checkbox"></div>
            <div class="skeleton-interest-text"></div>
        `;
        interestsContainer.appendChild(skeleton);
    }
    
    // Add 2-second delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Clear skeleton
    interestsContainer.innerHTML = '';
    interestsContainer.classList.add('interests-loaded');
    
    if (destinations.length === 0) {
        interestsContainer.innerHTML = '<p style="text-align: center; color: #666;">No interests available. Please select a destination.</p>';
        return;
    }
    
    // Create SEPARATE interest sections for each destination
    for (const destination of destinations) {
        const city = destination.name.split(',')[0].trim(); // Extract city name
        
        // Create destination section wrapper
        const destSection = document.createElement('div');
        destSection.className = 'destination-section';
        
        // Create destination header
        const destHeader = document.createElement('div');
        destHeader.className = 'destination-interests-header';
        destHeader.innerHTML = `
            <h4>
                📍 ${city} (${destination.code})
            </h4>
        `;
        destSection.appendChild(destHeader);
        
        // Get interests for this destination
        let availableInterests = [];
        
        try {
            // Try AI first for Pro users
            if (currentPlan === 'pro') {
                const aiInterests = await getAIInterestsForCity(city, destination.code);
                availableInterests = aiInterests;
            }
        } catch (error) {
            console.log('Using fallback interests for', city);
        }
        
        // Fallback to city-specific or country interests
        if (availableInterests.length === 0) {
            const country = destination.name.split(',')[1]?.trim();
            availableInterests = cityInterests[city] || 
                                countryInterests[country] || 
                                countryInterests.default;
            availableInterests = availableInterests.slice(0, 12);
        }
        
        // Create interest options for this destination
        const destInterestsContainer = document.createElement('div');
        destInterestsContainer.className = 'destination-interests-group';
        
        availableInterests.forEach(interest => {
            const option = document.createElement('div');
            option.className = 'checkbox-option';
            option.dataset.destination = destination.code;
            option.innerHTML = `
                <input type="checkbox" value="${interest.replace(/\s*[^\w\s]+\s*$/, '').trim()}" 
                       data-destination="${destination.code}">
                <span>${interest}</span>
            `;
            
            option.addEventListener('click', function(e) {
                if (e.target.tagName !== 'INPUT') {
                    this.classList.toggle('selected');
                    const checkbox = this.querySelector('input');
                    checkbox.checked = !checkbox.checked;
                    updateSelectedInterests();
                } else {
                    this.classList.toggle('selected');
                    updateSelectedInterests();
                }
            });
            
            destInterestsContainer.appendChild(option);
        });
        
        destSection.appendChild(destInterestsContainer);
        interestsContainer.appendChild(destSection);
    }
    
    console.log('Separate interests displayed for each destination');
}

// New helper function to get AI interests for specific city
async function getAIInterestsForCity(city, code) {
    try {
        const response = await fetch('/get-ai-interests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                destinations: [city],
                airportCode: code
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get AI interests');
        }
        
        const data = await response.json();
        return data.interests || [];
    } catch (error) {
        console.error('Error getting AI interests for', city, error);
        throw error;
    }
}

function updateSelectedInterests() {
    const selectedInterests = Array.from(document.querySelectorAll('.checkbox-option.selected'))
        .map(option => {
            const value = option.querySelector('input').value;
            // Strip emoji from the end if present
            return value.replace(/\s*[^\w\s]+\s*$/, '').trim();
        });
    
    document.getElementById('interests').value = selectedInterests.join(', ');
}

// Date validation
function updateEndDateMin() {
    const startDate = document.getElementById('start-date').value;
    if (startDate) {
        document.getElementById('end-date').min = startDate;
    }
}

// Form submission handler
async function handleFormSubmit(e) {
    e.preventDefault();
    
    console.log('✅ handleFormSubmit called');
    console.log('Step 1: Checking authentication...');
    
    try {
        // Check authentication first
        const authCheck = await fetch('/auth/check');
        console.log('Auth response status:', authCheck.status);
        const authData = await authCheck.json();
        console.log('Auth data:', authData);
        
        if (!authData.authenticated) {
            alert('Please log in to generate itineraries');
            window.location.href = '/';
            return;
        }
        
        console.log('Step 2: Checking usage limits...');
        // Check free plan usage
        if (authData.user.plan === 'free') {
            const usageCheck = await fetch('/get-usage');
            const usageData = await usageCheck.json();
            console.log('Usage data:', usageData);
            
            if (usageData.free_uses_remaining <= 0) {
                alert('You have reached your daily limit of 3 free itineraries. Please upgrade to Pro for unlimited access.');
                return;
            }
        }
        
        console.log('Step 3: Validating form...');
        // Validate form
        if (!validateForm()) {
            console.log('❌ Form validation failed');
            return;
        }
        
        console.log('Step 4: Showing loading screen...');
        // Show loading section
        document.getElementById('form-section').style.display = 'none';
        document.getElementById('loading-section').style.display = 'block';
        document.getElementById('result-section').style.display = 'none';
        
        console.log('Step 5: Getting form data...');
        // Get form data and send to backend
        const formData = getFormData();
        console.log('Form data:', formData);
        
        console.log('Step 6: Sending to backend...');
        const response = await fetch('/generate-itinerary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        console.log('Response status:', response.status);
        const result = await response.json();
        console.log('Result:', result);
        
        if (!response.ok) {
            throw new Error(result.error || `Server error: ${response.status}`);
        }
        
        if (result.success) {
            console.log('✅ Success! Displaying itinerary...');
            // Update usage counter
            freeUsesRemaining = result.free_uses_remaining;
            updateUsageCounter();
            
            // Display the AI-generated itinerary
            displayItinerary(result.itinerary, formData);
            
            // Search and display flights - ADD THIS
            searchAndDisplayFlights(formData);
        } else {
            throw new Error(result.error || 'Failed to generate itinerary');
        }
        
    } catch (error) {
        console.error('❌ Error generating itinerary:', error);
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
    if (!userName) {
        console.error('❌ user-name field not found');
        alert('Form error: Name field not found');
        return false;
    }
    if (!userName.value || !userName.value.trim()) {
        alert('Please enter your name');
        userName.focus();
        return false;
    }
    console.log('✅ User name valid:', userName.value);

    // Check departure city - ADD THIS
    const departureCity = document.getElementById('departure-city');
    if (!departureCity || !departureCity.value) {
        alert('Please select your departure city');
        document.getElementById('departure-city-search').focus();
        return false;
    }
    
    // Check destinations
    const destinationInputs = document.querySelectorAll('.destination-value');
    console.log('Found destination inputs:', destinationInputs.length);
    
    const destinations = Array.from(destinationInputs)
        .map(input => input.value)
        .filter(value => value && value.trim());
    
    console.log('Valid destinations:', destinations);
    
    if (destinations.length === 0) {
        alert('Please select at least one destination');
        return false;
    }
    
    // Check dates
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    if (!startDate || !startDate.value) {
        alert('Please select a start date');
        if (startDate) startDate.focus();
        return false;
    }
    console.log('✅ Start date valid:', startDate.value);
    
    if (!endDate || !endDate.value) {
        alert('Please select an end date');
        if (endDate) endDate.focus();
        return false;
    }
    console.log('✅ End date valid:', endDate.value);
    
    // Check date validity
    const start = new Date(startDate.value);
    const end = new Date(endDate.value);
    
    if (end <= start) {
        alert('End date must be after start date');
        return false;
    }
    
    // Check traveler type
    const travelerType = document.getElementById('traveler-type');
    if (!travelerType || !travelerType.value) {
        alert('Please select a traveler type');
        return false;
    }
    console.log('✅ Traveler type valid:', travelerType.value);
    
    // Check currency
    const currency = document.getElementById('currency');
    if (!currency || !currency.value) {
        alert('Please select a currency');
        return false;
    }
    console.log('✅ Currency valid:', currency.value);
    
    // Check budget amount
    const budgetAmount = document.getElementById('budget-amount');
    if (!budgetAmount || !budgetAmount.value || parseFloat(budgetAmount.value) <= 0) {
        alert('Please enter a valid budget amount');
        if (budgetAmount) budgetAmount.focus();
        return false;
    }
    console.log('✅ Budget valid:', budgetAmount.value);
    
    console.log('✅ Form validation passed!');
    return true;
}

// In index.js - Update the getFormData function to ensure traveler type is properly sent
function getFormData() {
    const destinationItems = document.querySelectorAll('.destination-item');
    const destinations = [];
    const destinationCodes = [];
    
    destinationItems.forEach(item => {
        const name = item.querySelector('.destination-value').value;
        const code = item.querySelector('.destination-code').value;
        if (name && code) {
            destinations.push(name);
            destinationCodes.push(code);
        }
    });
    
    const interests = Array.from(document.querySelectorAll('.checkbox-option.selected'))
        .map(option => option.querySelector('input').value);
    
    const planField = document.getElementById('user-plan');
    const budgetFriendlyCheckbox = document.getElementById('budget-friendly');
    
    // Get traveler type - ensure it's properly captured
    const travelerType = document.getElementById('traveler-type').value;
    console.log('📝 Traveler type being sent:', travelerType);
    
    return {
        userName: document.getElementById('user-name').value,
        plan: planField ? planField.value : currentPlan,
        budgetFriendly: budgetFriendlyCheckbox ? budgetFriendlyCheckbox.checked : false,
        departureCity: document.getElementById('departure-city').value,
        departureCityCode: document.getElementById('departure-city-code').value,
        destinations: destinations,
        destinationCodes: destinationCodes,
        startDate: document.getElementById('start-date').value,
        endDate: document.getElementById('end-date').value,
        travelerType: travelerType, // This should now be properly captured
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
        const startDate = new Date(formData.startDate);
        const endDate = new Date(formData.endDate);
        const duration = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1;
        
        summaryText.textContent = `This ${duration}-day ${formData.travelerType.toLowerCase()} trip to ${formData.destinations.join(' and ')} is perfectly crafted for your interests in ${formData.interests}. With a budget of ${formData.currencySymbol}${formData.budget.toLocaleString()}, you'll experience the best of local culture, cuisine, and attractions. ${formData.notes ? `Special notes: ${formData.notes}` : ''}`;
    }
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    const userName = document.getElementById('user-name').value || 'Traveler';
    const destinations = Array.from(document.querySelectorAll('.destination-value'))
        .map(input => input.value)
        .filter(value => value);
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const budget = document.getElementById('budget-amount').value;
    const currencySymbol = document.getElementById('currency-symbol').value;
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    const duration = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    
    doc.setProperties({
        title: `TripStar Itinerary - ${destinations.join(', ')}`,
        subject: 'AI-Generated Travel Itinerary',
        author: 'TripStar AI'
    });
    
    const pageWidth = doc.internal.pageSize.width;
    const pageHeight = doc.internal.pageSize.height;
    const margin = 20;
    const contentWidth = pageWidth - (2 * margin);
    
    let currentPage = 1;
    let yPosition = 25;
    
    // Header
    doc.setFillColor(70, 130, 180);
    doc.circle(23, 20, 3, 'F');
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(22);
    doc.setFont('helvetica', 'bold');
    doc.text('TripStar AI', 30, 23);
    
    doc.setFontSize(9);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(100, 100, 100);
    doc.text('Smart AI-Powered Itinerary Generator', margin, 32);
    
    yPosition = 50;
    doc.setFontSize(20);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(0, 0, 0);
    doc.text(`Your ${destinations[0] || 'Destination'} Itinerary`, margin, yPosition);
    
    yPosition = 70;
    
    const dayCards = document.querySelectorAll('.day-card');
    
    dayCards.forEach((dayCard, dayIndex) => {
        if (yPosition > 210) {
            addFooter(doc, currentPage);
            doc.addPage();
            currentPage++;
            yPosition = 25;
        }
        
        const dayHeader = cleanText(dayCard.querySelector('.day-header')?.textContent || `Day ${dayIndex + 1}`);
        const dayTitle = cleanText(dayCard.querySelector('h3')?.textContent || `Day ${dayIndex + 1} Activities`);
        const dayDesc = cleanText(dayCard.querySelector('p')?.textContent || 'Daily activities.');
        
        doc.setFillColor(240, 240, 240);
        doc.roundedRect(margin, yPosition - 3.5, 6, 6, 1, 1, 'F');
        doc.setFillColor(0, 0, 0);
        doc.setFontSize(8);
        doc.setFont('helvetica', 'bold');
        doc.text('D', margin + 2, yPosition + 1.5);
        
        doc.setFontSize(11);
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(0, 0, 0);
        doc.text(dayHeader, margin + 9, yPosition + 1);
        yPosition += 10;
        
        doc.setFontSize(13);
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
        
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        const overviewLabel = 'Overview: ';
        doc.text(overviewLabel, margin, yPosition);
        
        doc.setFont('helvetica', 'normal');
        const overviewText = dayDesc.replace(/^Overview:\s*/i, '');
        const overviewLines = doc.splitTextToSize(overviewText, contentWidth);
        
        overviewLines.forEach((line, idx) => {
            if (yPosition > 265) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            doc.text(line, margin + (idx === 0 ? doc.getTextWidth(overviewLabel) : 0), yPosition);
            yPosition += 4.5;
        });
        
        yPosition += 4;
        
        doc.setFontSize(9);
        doc.setFont('helvetica', 'bold');
        doc.text('Daily Activities:', margin, yPosition);
        yPosition += 6;
        
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
            
            doc.text("✓", margin, yPosition);
            
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
        
        const dayTip = cleanText(dayCard.querySelector('.pro-section p')?.textContent || '');
        if (dayTip) {
            if (yPosition > 240) {
                addFooter(doc, currentPage);
                doc.addPage();
                currentPage++;
                yPosition = 25;
            }
            
            doc.setFillColor(255, 215, 0);
            doc.circle(margin + 3, yPosition + 1, 2.5, 'F');
            
            doc.setFillColor(0, 0, 0);
            doc.setFontSize(8);
            doc.setFont('helvetica', 'bold');
            doc.text('!', margin + 2.5, yPosition + 2.5);
            
            doc.setFontSize(10);
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
    
    if (yPosition > 170) {
        addFooter(doc, currentPage);
        doc.addPage();
        currentPage++;
        yPosition = 25;
    }
    
    doc.setFillColor(255, 100, 0);
    doc.circle(margin + 3, yPosition + 1.5, 2.5, 'F');
    
    doc.setFontSize(13);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(0, 0, 0);
    doc.text('Currently Trending', margin + 9, yPosition + 2.5);
    yPosition += 12;
    
    const spotCards = document.querySelectorAll('.spot-card');
    spotCards.forEach((spotCard, index) => {
        if (yPosition > 240) {
            addFooter(doc, currentPage);
            doc.addPage();
            currentPage++;
            yPosition = 25;
        }
        
        const spotName = cleanText(spotCard.querySelector('h4')?.textContent || `Popular Spot ${index + 1}`);
        const spotDesc = cleanText(spotCard.querySelector('p')?.textContent || 'Explore this destination.');
        
        doc.setFontSize(11);
        doc.setFont('helvetica', 'bold');
        doc.text(spotName, margin, yPosition);
        yPosition += 6;
        
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
    
    if (yPosition > 220) {
        addFooter(doc, currentPage);
        doc.addPage();
        currentPage++;
        yPosition = 25;
    }
    
    doc.setFillColor(200, 200, 200);
    doc.roundedRect(margin, yPosition - 2, 5, 6, 1, 1, 'F');
    
    doc.setFontSize(13);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(0, 0, 0);
    doc.text('Trip Summary', margin + 8, yPosition + 2);
    yPosition += 10;
    
    const summaryElement = document.getElementById('summary-text');
    const summaryText = cleanText(summaryElement?.textContent || 'Enjoy your journey!');
    
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
    
    addFooter(doc, currentPage);
    
    const filename = `tripstar-itinerary-${destinations[0]?.toLowerCase().replace(/\s+/g, '-') || 'trip'}.pdf`;
    doc.save(filename);
}

function cleanText(text) {
    if (!text) return '';
    return text
        .replace(/\s+/g, ' ')
        .replace(/Overview:\s*Overview:/gi, 'Overview:')
        .replace(/[^\x20-\x7E]/g, ' ')
        .trim();
}

function addFooter(doc, pageNumber) {
    const pageWidth = doc.internal.pageSize.width;
    const pageHeight = doc.internal.pageSize.height;
    const margin = 20;
    const footerY = pageHeight - 10;
    
    doc.setFontSize(8);
    doc.setTextColor(120, 120, 120);
    doc.setFont('helvetica', 'normal');
    
    const year = new Date().getFullYear();
    
    doc.text(`© ${year} TripStar AI`, margin, footerY, { align: 'left' });
    doc.text('Smart AI-Powered Itinerary Generator', pageWidth / 2, footerY, { align: 'center' });
    doc.text(`Page ${pageNumber}`, pageWidth - margin, footerY, { align: 'right' });
}

function shareViaWhatsApp() {
    if (currentPlan === 'free') {
        alert('WhatsApp sharing is available for Pro users only.');
        return;
    }
    
    const itineraryText = `Check out my TripStar AI itinerary!`;
    const encodedText = encodeURIComponent(itineraryText);
    const whatsappUrl = `https://wa.me/?text=${encodedText}`;
    
    window.open(whatsappUrl, '_blank');
}

function resetForm() {
    document.getElementById('result-section').style.display = 'none';
    document.getElementById('form-section').style.display = 'block';
    
    document.getElementById('itinerary-form').reset();
    
    const destinationsContainer = document.getElementById('destinations-container');
    while (destinationsContainer.children.length > 1) {
        destinationsContainer.removeChild(destinationsContainer.lastChild);
    }
    
    document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
    document.querySelector('.traveler-type .option-btn[data-value="Solo"]')?.classList.add('selected');
    document.getElementById('traveler-type').value = 'Solo';
    
    const planField = document.getElementById('user-plan');
    if (planField) {
        planField.value = currentPlan;
    }
    
    document.getElementById('budget-friendly').checked = false;
    
    updateInterests();
    loadUsageData();
    setDefaultValues();
}

// Search and display flights
async function searchAndDisplayFlights(formData) {
    try {
        console.log('Searching for flights...');
        
        const response = await fetch('/search-flights', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                departure_city: formData.departureCity,
                destinations: formData.destinations,
                start_date: formData.startDate,
                end_date: formData.endDate,
                budget: formData.budget,
                currency_symbol: formData.currencySymbol
            })
        });
        
        const result = await response.json();
        
        if (result.success && result.flights) {
            displayFlightResults(result.flights);
        }
        
    } catch (error) {
        console.error('Flight search error:', error);
    }
}

function displayFlightResults(flightData) {
    console.log('📊 Flight data received:', flightData);
    
    let flightSection = document.getElementById('flight-results');
    if (!flightSection) {
        flightSection = document.createElement('div');
        flightSection.id = 'flight-results';
        flightSection.className = 'flight-results-section';
        const popularSpots = document.getElementById('popular-spots');
        popularSpots.parentNode.insertBefore(flightSection, popularSpots);
    }
    
    let flightHTML = `
        <div class="flight-header">
            <h3>✈️ Recommended Flights</h3>
            <a href="${flightData.searchLink || 'https://www.google.com/travel/flights'}" target="_blank" class="google-flights-btn">
                Search Real-time Flights
            </a>
        </div>
    `;
    
    if (flightData.flights && Array.isArray(flightData.flights)) {
        flightData.flights.forEach((flight, index) => {
            const departure = flight.departureCity || 'Your departure city';
            const destination = flight.destination || 'Destination';
            const outboundDate = flight.outboundDate || 'Select date';
            const segment = flight.segment || `Flight ${index + 1}`;
            
            flightHTML += `
                <div class="flight-destination-card">
                    <div class="flight-dest-header">
                        <h4>${segment}: ${departure} → ${destination}</h4>
                        <span class="flight-date">📅 ${outboundDate}</span>
                    </div>
                    
                    <div class="flight-options">
            `;
            
            if (flight.options && flight.options.length > 0) {
                flight.options.forEach(option => {
                    flightHTML += `
                        <div class="flight-option-card">
                            <div class="flight-option-header">
                                <div>
                                    <strong>${option.airline || 'Various Airlines'}</strong>
                                    <span class="flight-number">${option.flightNumber || 'Check availability'}</span>
                                </div>
                                <span class="flight-duration">⏱️ ${option.duration || 'Varies'}</span>
                            </div>
                            
                            <div class="flight-details">
                                <span class="flight-stops">🔄 ${option.stops || 0} stop(s)</span>
                                ${option.layover && option.layover !== 'None' ? `<span class="flight-layover">via ${option.layover}</span>` : ''}
                            </div>
                            
                            <div class="cabin-classes">
                    `;
                    
                    if (option.cabinClasses) {
                        Object.entries(option.cabinClasses).forEach(([className, classInfo]) => {
                            if (classInfo && classInfo.available !== false) {
                                flightHTML += `
                                    <div class="cabin-class">
                                        <span class="class-name">${className.replace(/([A-Z])/g, ' $1').trim()}</span>
                                        <span class="class-price">${classInfo.price || 'Check price'}</span>
                                        ${classInfo.seatsLeft ? `<span class="seats-left">${classInfo.seatsLeft} seats</span>` : ''}
                                    </div>
                                `;
                            }
                        });
                    }
                    
                    flightHTML += `
                            </div>
                            
                            <a href="${option.bookingLink || flightData.searchLink}" target="_blank" class="booking-link-single">
                                Check Real-time Availability →
                            </a>
                            
                            ${option.moneySavingTips ? `
                                <div class="flight-tips">
                                    <strong>💡 Money Saving Tips:</strong>
                                    <ul>
                                        ${option.moneySavingTips.map(tip => `<li>${tip}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </div>
                    `;
                });
            }
            
            flightHTML += `
                    </div>
                </div>
            `;
        });
    }
    
    // Add general tips
    flightHTML += `
        <div class="general-flight-tips">
            <h4>💡 Smart Booking Tips</h4>
            <ul>
                ${(flightData.generalTips || [
                    'Book multi-city flights as single itinerary for best pricing',
                    'Compare prices across different booking platforms',
                    'Be flexible with dates for significant savings',
                    'Check baggage policies for each airline segment'
                ]).map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `;
    
    flightSection.innerHTML = flightHTML;
}