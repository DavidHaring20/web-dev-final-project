console.log("app.js");
// Global Variables
const USER_ID = String;

// Buttons
const signupSubmitButton = document.getElementById('submit-signup');
const loginSubmitButton = document.getElementById('submit-login');

// Signup
signupSubmitButton.addEventListener('click', () => {
    // Create form data
    const form = new FormData();
    // Get data from form and append it to form data
    form.append('first-name', document.querySelector('.signup-modal-form-first-name-input').value);
    if (document.querySelector('.signup-modal-form-middle-name-input').value)
        form.append('middle-name', document.querySelector('.signup-modal-form-middle-name-input').value); 
    form.append('last-name', document.querySelector('.signup-modal-form-last-name-input').value); 
    form.append('address', document.querySelector('.signup-modal-form-address-input').value); 
    form.append('age', document.querySelector('.signup-modal-form-age-input').value); 
    form.append('username', document.querySelector('.signup-modal-form-username-input').value); 
    form.append('email', document.querySelector('.signup-modal-form-email-input').value); 
    form.append('password', document.querySelector('.signup-modal-form-password-input').value); 
    form.append('password-retype', document.querySelector('.signup-modal-form-retype-password-input').value); 
    
    // Call async function with fetch
    signup(form);
});

async function signup(form) {
    fetch('/api/users', {
        method: 'POST',
        body: form
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success",data);
        if (data.userAdded) {
            goToLanding();
        }
    })
    .catch((error) => {
        console.log("Error", error);
    })
};

// Login
loginSubmitButton.addEventListener('click', () => {
    // Get data from form
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
     // Create form data
     const form = new FormData();
     form.append('email', email);
     form.append('password', password);
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
        if (data.login) {
            USER_ID = data.UserId;
            goToHome()
        }
    })
    .catch((error) => {
        console.log("Error", error);
    })
} 