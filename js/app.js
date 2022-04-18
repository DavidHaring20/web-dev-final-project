console.log("app.js");
// Global Variables
const USER_ID = String;

/////////////////////////////////////////////////
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