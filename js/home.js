// Elements
const userInfo = document.querySelector('.home-page-column-1-user-info');
const logoutButton = document.querySelector('.home-page-column-1-pop-up-3');

userInfo.addEventListener('click', () => {
    console.log("user-info")
    // Scroll 
    window.scroll(0, 0);
    body.classList.add('focused');
    // Open home overlay
    openHomeOverlay();
    // Open logoutPopup window
    openLogoutPopup();
});

logoutButton.addEventListener('click', () => {
    // Make button disabled
    logoutButton.disabled = true;
    logoutButton.innerText = "Logging out @";
    // Call fetch method
    logout(USER_ID);
});

homeOverlay.addEventListener('click', () => {
    // Hide Home overlay
    if (!homeOverlay.classList.contains('hidden'))
        homeOverlay.classList.add('hidden');
    body.classList.remove('focused');
    // Hide logout pop-up
    closeLogoutPopup();
    // Hide tweet form pop-up
    closeTweetFormPopup();
    // Hide delete tweet pop-up
    closeTweetDeletePopup();
});

async function logout(id) {
    // Fetch
    // fetch('/api/sessions/' + id, {
    fetch('/api/sessions/' + '6facbefe-5493-4011-b58e-04aa69515bba', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);

        // 200 OK
        if (data.logout) {
            // Close Home overlay
            closeHomeOverlay();

            // Close Logout pop-up
            closeLogoutPopup();
            
            // Open Landing page
            goToLanding();
        }
        
        // Make button enabled
        logoutButton.disabled = false;
        logoutButton.innerText = "Log out @";
    })
    .catch((error) => {
        console.log("Error", error);
    });
}