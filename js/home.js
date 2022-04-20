console.log("home.js");

// Elements
const userInfo = document.querySelector('.home-page-column-1-user-info');

userInfo.addEventListener('click', () => {
    console.log("user-info")
    // Open home overlay
    openHomeOverlay();
    // Open logoutPopup window
    openLogoutPopup();
});

logoutPopup.addEventListener('click', () => {
    console.log('popup1')
});

homeOverlay.addEventListener('click', () => {
    // Hide Home overlay
    if (!homeOverlay.classList.contains('hidden'))
        homeOverlay.classList.add('hidden');
    // Hide logout pop-up
    if (logoutPopup.classList.contains('home-page-column-1-pop-up')) {
        logoutPopup.classList.remove('home-page-column-1-pop-up');
        logoutPopup.classList.add('hidden');
    }
});