console.log("navigation.js");
// Pages
const landingPage = document.getElementById('landing-page');
const loginPage = document.getElementById('login-page');
const signupPage = document.getElementById('signup-page');
const homePage = document.getElementById('home-page');

// Hide all other pages
loginPage.classList.add('hidden');
signupPage.classList.add('hidden');
homePage.classList.add('hidden');


// Go to Signup Page
function goToSignup() {
    // From Landing Page
    if (!landingPage.classList.contains('hidden'))
        landingPage.classList.add('hidden');
    signupPage.classList.remove('hidden');
}

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