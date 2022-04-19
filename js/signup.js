console.log("signup.js");
// Error message
const signupErrorMessage = document.querySelector('.signup-error-message');

// Form pages
const page1 = document.querySelector('.signup-modal-form-page-1');
const page2 = document.querySelector('.signup-modal-form-page-2');
const page3 = document.querySelector('.signup-modal-form-page-3');

// Buttons
const signupSubmitButton = document.getElementById('submit-signup');
const loginSubmitButton = document.getElementById('submit-login');

/////////////////////////////////////////////////
// Hide other pages
page2.classList.add('hidden');
page3.classList.add('hidden');

/////////////////////////////////////////////////
// Navigation in form pages
// 2 -> 1
function toPage1() {
    page2.classList.add('hidden');
    page1.classList.remove('hidden');
};

// 1 -> 2 or 3 -> 2
function toPage2() {
    if (!page3.classList.contains('hidden')) {
        page3.classList.add('hidden');
    }
    if (!page1.classList.contains('hidden')) {
        page1.classList.add('hidden');
    }
    page2.classList.remove('hidden');
};

// 2 -> 3
function toPage3() {
    page2.classList.add('hidden');
    page3.classList.remove('hidden');
};


/////////////////////////////////////////////////
// Signup
signupSubmitButton.addEventListener('click', () => {
    signupSubmitButton.disabled = true;
    signupSubmitButton.innerText = 'Please wait';
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
        // OK 200
        if (data.userAdded) {
            goToLanding();
            signupErrorMessage.innerText = '';
        }
        // 40x and 50x
        if (data.errorMessage) {
            signupErrorMessage.innerText = data.errorMessage;
        }
        signupSubmitButton.disabled = false;
        signupSubmitButton.innerText = 'Sign up';
    })
    .catch((error) => {
        console.log("Error", error);
    })
};