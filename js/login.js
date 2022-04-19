console.log('login.js')
/////////////////////////////////////////////////
// Login
loginSubmitButton.addEventListener('click', () => {
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
        if (data.login) {
            USER_ID = data.UserId;
            goToHome()
        }
    })
    .catch((error) => {
        console.log("Error", error);
    })
} 