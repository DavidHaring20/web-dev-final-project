console.log("navigation.js");
// Pages
const landingPage = document.getElementById('landing-page');
const loginPage = document.getElementById('login-page');
const homePage = document.getElementById('home-page');

// Buttons
const signupExitButton = document.getElementById('signup-exit');

// Modals
const signupLogin = document.getElementById('signup-modal');

// Overlays
const darkOverlay = document.getElementById('signup-overlay');

// Hide all other pages and modals
loginPage.classList.add('hidden');
homePage.classList.add('hidden');
darkOverlay.classList.add('hidden');
signupLogin.classList.add('hidden');


// Go to Signup Page
function goToSignup() {
    darkOverlay.classList.remove('hidden');
    signupLogin.classList.remove('hidden');
}

// Go to Landing Page
function goToLanding() {
    // From Signup Page
    if (!darkOverlay.classList.contains('hidden'))
        darkOverlay.classList.add('hidden');
    if (!signupLogin.classList.contains('hidden'))
        signupLogin.classList.add('hidden');
};

// Go to Login Page
function goToLogin() {
    // From Landing Page
    if (!landingPage.classList.contains('hidden'))
        landingPage.classList.add('hidden');
    loginPage.classList.remove('hidden');
}

// Go to Home Page
function goToHome () {
    console.log('GO hOMe')
    // From Login Page
    if (!loginPage.classList.contains('hidden'))
        loginPage.classList.add('hidden');
    homePage.classList.remove('hidden');
}

// Methods
signupExitButton.addEventListener('click', () => {
    goToLanding();
});