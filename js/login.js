// Error message
const loginErrorMessage = document.querySelector('.login-modal-error-message');

// User informations in Home page
const userNameAndSurnameH3 = document.getElementById('home-page-column-1-user-info-logout-user-names-name')
const userUsernameP = document.getElementById('home-page-column-1-user-info-logout-user-names-username')

/////////////////////////////////////////////////
// Login
loginSubmitButton.addEventListener('click', () => {
    // Disable log in button
    loginSubmitButton.disabled = true;
    loginSubmitButton.innerText = 'Logging in';
    // Get data from form and create form data
    const form = new FormData();
    form.append('email', document.getElementById('email').value);
    form.append('password', document.getElementById('password').value);
    login(form)
});
async function login(form) {
    // Fetch
    fetch('/api/sessions', {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success", data);
        // OK 200
        if (data.login) {
            USER_ID = data.userId;
            if (data.userRole === "admin") {
                apiGetAllTweets()
                goToAdminPage()
            } else {

                USER_NAME = data.userName;
                USER_SURNAME = data.userSurname;
                USER_USERNAME = data.userUsername;
                
                // Set user information in Home page
                userNameAndSurnameH3.innerText = `${data.userName} ${data.userSurname}`
                userUsernameP.innerText = `${data.userUsername}`
                // document.querySelector('.home-page-column-1-user-info-logout-user-names-name').innerHTML = `${data.userName} ${USER_SURNAME}`
                
                // Get User tweets and Followed/Non-Followed
                getTweetByUserID(data.userId)
                apiGetUsers(data.userId)
                // Open Column 3 on Home Page
                openColumn3()
                // Open loading screen
                goToHome();
            }
        }

        // 40x 50x
        if (data.errorMessage) {
            loginErrorMessage.innerText = data.errorMessage;
        }
        // Enable login button
        loginSubmitButton.disabled = false;
        loginSubmitButton.innerText = 'Log in';
    })
    .catch((error) => {
        console.log("Error", error);
    })
} 