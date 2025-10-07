// Welcome Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const loginBtn = document.getElementById('login-btn');
    const signupBtn = document.getElementById('signup-btn');
    const dashboardBtn = document.getElementById('dashboard-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const getStartedBtn = document.getElementById('get-started-btn');
    const authModal = document.getElementById('auth-modal');
    const planModal = document.getElementById('plan-modal');
    const closeModalBtns = document.querySelectorAll('.close-btn');
    const closePlanModalBtn = document.getElementById('close-plan-modal');
    const switchLink = document.getElementById('switch-link');
    const switchText = document.getElementById('switch-text');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const modalTitle = document.getElementById('modal-title');
    const planSelectBtns = document.querySelectorAll('.plan-select-btn');
    const selectPlanBtns = document.querySelectorAll('.select-plan-btn');
    const planOptions = document.querySelectorAll('.plan-option');
    const navActions = document.getElementById('nav-actions');

    // Check if user is already logged in and update UI
    checkAuthStatus();

    // Event Listeners
    loginBtn.addEventListener('click', () => showAuthModal('login'));
    signupBtn.addEventListener('click', () => showAuthModal('register'));
    dashboardBtn.addEventListener('click', () => {
        window.location.href = '/dashboard';
    });
    logoutBtn.addEventListener('click', handleLogout);
    
    getStartedBtn.addEventListener('click', () => {
        // Directly select free plan and show registration
        selectPlan('free');
    });
    
    closeModalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            authModal.classList.remove('active');
            planModal.classList.remove('active');
        });
    });
    
    closePlanModalBtn.addEventListener('click', () => {
        planModal.classList.remove('active');
    });

    switchLink.addEventListener('click', (e) => {
        e.preventDefault();
        toggleAuthForms();
    });

    // Auth form submissions
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);

    // Plan selection
    planSelectBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const plan = e.target.dataset.plan;
            selectPlan(plan);
        });
    });

    selectPlanBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const planOption = e.target.closest('.plan-option');
            const plan = planOption.dataset.plan;
            selectPlan(plan);
        });
    });

    planOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            if (!e.target.classList.contains('select-plan-btn')) {
                const plan = option.dataset.plan;
                const selectBtn = option.querySelector('.select-plan-btn');
                selectBtn.click();
            }
        });
    });

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === authModal) {
            authModal.classList.remove('active');
        }
        if (e.target === planModal) {
            planModal.classList.remove('active');
        }
    });

    // Functions
    function checkAuthStatus() {
        fetch('/auth/check')
            .then(response => response.json())
            .then(data => {
                updateUIForAuthState(data.authenticated);
            })
            .catch(error => {
                console.error('Auth check failed:', error);
                updateUIForAuthState(false);
            });
    }

    function updateUIForAuthState(isAuthenticated) {
        if (isAuthenticated) {
            // User is logged in - show dashboard and logout buttons
            loginBtn.style.display = 'none';
            signupBtn.style.display = 'none';
            dashboardBtn.style.display = 'block';
            logoutBtn.style.display = 'block';
            
            // Update get started button to go directly to dashboard
            getStartedBtn.innerHTML = 'Go to Dashboard <i class="fas fa-arrow-right"></i>';
            getStartedBtn.onclick = () => window.location.href = '/dashboard';
        } else {
            // User is not logged in - show login/signup buttons
            loginBtn.style.display = 'block';
            signupBtn.style.display = 'block';
            dashboardBtn.style.display = 'none';
            logoutBtn.style.display = 'none';
            
            // Reset get started button
            getStartedBtn.innerHTML = 'Get Started Free <i class="fas fa-arrow-right"></i>';
            getStartedBtn.onclick = () => selectPlan('free');
        }
    }

    function handleLogout() {
        fetch('/auth/logout')
            .then(response => {
                if (response.ok) {
                    showNotification('Logged out successfully!', 'success');
                    // Clear any pending plans
                    localStorage.removeItem('pendingPlan');
                    // Update UI
                    updateUIForAuthState(false);
                    // Reload to clear any state
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    throw new Error('Logout failed');
                }
            })
            .catch(error => {
                console.error('Logout error:', error);
                showNotification('Logout failed', 'error');
            });
    }

    function showAuthModal(type) {
        if (type === 'login') {
            showLoginForm();
        } else {
            showRegisterForm();
        }
        authModal.classList.add('active');
    }

    function showPlanModal() {
        planModal.classList.add('active');
    }

    function toggleAuthForms() {
        if (loginForm.style.display === 'none') {
            showLoginForm();
        } else {
            showRegisterForm();
        }
    }

    function showLoginForm() {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        modalTitle.textContent = 'Welcome Back';
        switchText.innerHTML = 'Don\'t have an account? <a href="#" id="switch-link">Sign up</a>';
        // Re-attach event listener for the new switch link
        document.getElementById('switch-link').addEventListener('click', (e) => {
            e.preventDefault();
            toggleAuthForms();
        });
    }

    function showRegisterForm() {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        modalTitle.textContent = 'Create Account';
        switchText.innerHTML = 'Already have an account? <a href="#" id="switch-link">Sign in</a>';
        // Re-attach event listener for the new switch link
        document.getElementById('switch-link').addEventListener('click', (e) => {
            e.preventDefault();
            toggleAuthForms();
        });
    }

    function handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Login successful! Redirecting...', 'success');
                authModal.classList.remove('active');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                showNotification(data.error || 'Login failed', 'error');
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            showNotification('Login failed. Please try again.', 'error');
        });
    }

    function handleRegister(e) {
        e.preventDefault();
        
        const firstName = document.getElementById('first-name').value;
        const lastName = document.getElementById('last-name').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;

        fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                firstName: firstName,
                lastName: lastName,
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Registration successful! Welcome to TripStar AI.', 'success');
                authModal.classList.remove('active');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                showNotification(data.error || 'Registration failed', 'error');
            }
        })
        .catch(error => {
            console.error('Registration error:', error);
            showNotification('Registration failed. Please try again.', 'error');
        });
    }

    function selectPlan(plan) {
        if (!isAuthenticated()) {
            // If not authenticated, show auth modal first
            showAuthModal('register');
            // Store the selected plan for after registration
            localStorage.setItem('pendingPlan', plan);
            return;
        }

        // User is authenticated, update plan
        fetch('/update-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                plan: plan
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`Plan updated to ${plan}!`, 'success');
                planModal.classList.remove('active');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1000);
            } else {
                showNotification(data.error || 'Plan update failed', 'error');
            }
        })
        .catch(error => {
            console.error('Plan update error:', error);
            showNotification('Plan update failed. Please try again.', 'error');
        });
    }

    function isAuthenticated() {
        // This will be determined by the server response
        return document.body.getAttribute('data-authenticated') === 'true';
    }

    function showNotification(message, type) {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 3000;
            animation: slideIn 0.3s ease-out;
            max-width: 300px;
        `;
        
        if (type === 'success') {
            notification.style.background = 'var(--primary)';
        } else {
            notification.style.background = '#e74c3c';
        }
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOut 0.3s ease-in';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 3000);
    }

    // Add CSS for notifications
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        .nav-btn {
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            border: none;
            margin-left: 10px;
        }

        .dashboard-btn {
            background: var(--accent);
            color: white;
        }

        .dashboard-btn:hover {
            background: #e64a19;
        }

        .logout-btn {
            background: #6c757d;
            color: white;
        }

        .logout-btn:hover {
            background: #5a6268;
        }
    `;
    document.head.appendChild(style);
});