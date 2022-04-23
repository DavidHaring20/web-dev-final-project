// Body
const body = document.querySelector('body');

// Pages
const landingPage = document.getElementById('landing-page');
const homePage = document.getElementById('home-page');
const adminPage = document.getElementById('admin-page');
const column3 = document.querySelector('.home-page-column-3')

// Buttons
const signupExitButton = document.getElementById('signup-exit');
const loginExitButton = document.getElementById('login-exit');
const tweetCreateExitButton = document.getElementById('home-page-column-2-pop-up-tweet-form-header-close-button');

// Modals
const signupModal = document.getElementById('signup-modal');
const loginModal = document.getElementById('login-modal');

// Overlays
const signupOverlay = document.getElementById('signup-overlay');
const loginOverlay = document.getElementById('login-overlay');
const homeOverlay = document.getElementById('home-overlay');

// Pop-up windows
const logoutPopup = document.querySelector('.home-page-column-1-pop-up');
const tweetPopup = document.querySelector('.home-page-column-2-pop-up-tweet-form');
const deleteTweetPopup = document.querySelector('.home-page-column-2-pop-up-delete-tweet');
const followUnfollowPopup = document.getElementById('popup-3');

// Hide all other pages, overlays and modals
// landingPage.classList.add('hidden');
homePage.classList.add('hidden');
adminPage.classList.add('hidden');
homeOverlay.classList.add('hidden');
if (logoutPopup.classList.contains('home-page-column-1-pop-up')) {
    logoutPopup.classList.remove('home-page-column-1-pop-up');
    logoutPopup.classList.add('hidden');
}
if (tweetPopup.classList.contains('home-page-column-2-pop-up-tweet-form')) {
    tweetPopup.classList.remove('home-page-column-2-pop-up-tweet-form');
    tweetPopup.classList.add('hidden');
}
if (deleteTweetPopup.classList.contains('home-page-column-2-pop-up-delete-tweet')) {
    deleteTweetPopup.classList.remove('home-page-column-2-pop-up-delete-tweet');
    deleteTweetPopup.classList.add('hidden');
}
followUnfollowPopup.classList.remove('.home-page-column-3-follow-unfollow');
followUnfollowPopup.classList.add('hidden');
signupOverlay.classList.add('hidden');
signupModal.classList.add('hidden');
loginOverlay.classList.add('hidden');
loginModal.classList.add('hidden');
column3.classList.remove('home-page-column-3')
column3.classList.add('hidden')
/////////////////////////////////////////////////
// Methods 

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
// Close Home overlay
function closeHomeOverlay() {
    if (!homeOverlay.classList.contains('hidden'))
        homeOverlay.classList.add('hidden');
};
// Open Logout pop-up
function openLogoutPopup() {
    if (logoutPopup.classList.contains('hidden'))
        logoutPopup.classList.remove('hidden');
        logoutPopup.classList.add('home-page-column-1-pop-up');
};
// Close Logout pop-up
function closeLogoutPopup() {
    if (!logoutPopup.classList.contains('hidden'))
        logoutPopup.classList.add('hidden');
        logoutPopup.classList.remove('home-page-column-1-pop-up');
};
// Open Tweet form pop-up
function openTweetFormPopup() {
    if (tweetPopup.classList.contains('hidden')) {
        tweetPopup.classList.remove('hidden');
        tweetPopup.classList.add('home-page-column-2-pop-up-tweet-form');
    }
    window.scroll(0, 0);
    body.classList.add('focused');
};
// Close Tweet form pop-up
function closeTweetFormPopup() {
    if (!tweetPopup.classList.contains('hidden')) {
        tweetPopup.classList.add('hidden');
        tweetPopup.classList.remove('home-page-column-2-pop-up-tweet-form');
    }
    body.classList.remove('focused');
};
// Open Tweet delete pop-up
function openTweetDeletePopup() {
    if (!deleteTweetPopup.classList.contains('home-page-column-2-pop-up-delete-tweet')) {
        deleteTweetPopup.classList.add('home-page-column-2-pop-up-delete-tweet');
        deleteTweetPopup.classList.remove('hidden');
    }
    window.scroll(0, 0);
    body.classList.add('focused');
};
// Close Tweet delete pop-up
function closeTweetDeletePopup() {
    if (deleteTweetPopup.classList.contains('home-page-column-2-pop-up-delete-tweet')) {
        deleteTweetPopup.classList.remove('home-page-column-2-pop-up-delete-tweet');
        deleteTweetPopup.classList.add('hidden');
    }
    body.classList.remove('focused');
};

// Open Follow/Unfollow
function openFollowUnfollowPopup() {
    followUnfollowPopup.classList.add('home-page-column-3-follow-unfollow');
    followUnfollowPopup.classList.remove('hidden');
    window.scroll(0, 0);
    body.classList.add('focused');
}

// Close Follow/Unfollow
function closeFollowUnfollow() {
    followUnfollowPopup.classList.remove('home-page-column-3-follow-unfollow');
    followUnfollowPopup.classList.add('hidden');
    body.classList.remove('focused');
}
// Open Column 3
function openColumn3() {
    column3.classList.add('home-page-column-3')
    column3.classList.remove('hidden')
}

// Close Column 3
function closeColumn3() {
    column3.classList.remove('home-page-column-3')
    column3.classList.add('hidden')
}

function goToTweetForm() {
    openHomeOverlay();
    openTweetFormPopup();
}

/////////////////////////////////////////////////
// Event Listeners
signupExitButton.addEventListener('click', () => {
    goToLanding();
});

loginExitButton.addEventListener('click', () => {
    goToLanding();
});