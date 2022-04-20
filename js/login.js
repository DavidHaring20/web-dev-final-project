console.log('login.js')

// Error message
const loginErrorMessage = document.querySelector('.login-modal-error-message');

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
            USER_ID = data.UserId;
            USER_NAME = data.userName;
            USER_SURNAME = data.userSurname;
            USER_USERNAME = data.userUsername;
            goToHome();
            // getTweetByUserID();
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