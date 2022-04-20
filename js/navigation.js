console.log("navigation.js");
// Pages
const landingPage = document.getElementById('landing-page');
const homePage = document.getElementById('home-page');

// Buttons
const signupExitButton = document.getElementById('signup-exit');
const loginExitButton = document.getElementById('login-exit');

// Modals
const signupModal = document.getElementById('signup-modal');
const loginModal = document.getElementById('login-modal');

// Overlays
const signupOverlay = document.getElementById('signup-overlay');
const loginOverlay = document.getElementById('login-overlay');
const homeOverlay = document.getElementById('home-overlay');

// Pop-up windows
const logoutPopup = document.querySelector('.home-page-column-1-pop-up');

// Hide all other pages, overlays and modals
landingPage.classList.add('hidden');
// homePage.classList.add('hidden');
homeOverlay.classList.add('hidden');
if (logoutPopup.classList.contains('home-page-column-1-pop-up')) {
    logoutPopup.classList.remove('home-page-column-1-pop-up');
    logoutPopup.classList.add('hidden');
}
signupOverlay.classList.add('hidden');
signupModal.classList.add('hidden');
loginOverlay.classList.add('hidden');
loginModal.classList.add('hidden');


// Go to Signup Page
function goToSignup() {
    signupOverlay.classList.remove('hidden');
    signupModal.classList.remove('hidden');
}

// Go to Landing Page
function goToLanding() {
    // From Signup Page
    if (!signupOverlay.classList.contains('hidden'))
        signupOverlay.classList.add('hidden');
    if (!signupModal.classList.contains('hidden'))
        signupModal.classList.add('hidden');
    // From Login Page
    if (!loginOverlay.classList.contains('hidden'))
        loginOverlay.classList.add('hidden')
    if (!loginModal.classList.contains('hidden'))
        loginModal.classList.add('hidden')
    // Unhide Landing page
    if (landingPage.classList.contains('hidden'))
        landingPage.classList.remove('hidden');
};

// Go to Login Page
function goToLogin() {
    // From Landing Page
    if (!landingPage.classList.contains('hidden'))
        landingPage.classList.add('hidden');
    // Remove hidden on Login overlay and Login modal
    if (loginOverlay.classList.contains('hidden'))
        loginOverlay.classList.remove('hidden');
    if (loginModal.classList.contains('hidden'))
        loginModal.classList.remove('hidden');
}

// Go to Home Page
function goToHome () {
    console.log('GO hOMe')
    // From Login Page
    if (!loginOverlay.classList.contains('hidden'))
        loginOverlay.classList.add('hidden');
    if (!loginModal.classList.contains('hidden'))
        loginModal.classList.add('hidden');
    homePage.classList.remove('hidden');
}

// Open Home overlay
function openHomeOverlay() {
    if (homeOverlay.classList.contains('hidden'))
        homeOverlay.classList.remove('hidden');
};
function openLogoutPopup() {
    if (logoutPopup.classList.contains('hidden'))
        logoutPopup.classList.remove('hidden');
        logoutPopup.classList.add('home-page-column-1-pop-up');
};

// Methods
signupExitButton.addEventListener('click', () => {
    goToLanding();
});

loginExitButton.addEventListener('click', () => {
    goToLanding();
});