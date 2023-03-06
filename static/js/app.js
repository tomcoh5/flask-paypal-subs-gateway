// Get references to form elements
const registrationForm = document.getElementById("registration-form");
const loginForm = document.getElementById("login-form");
const registrationEmail = document.getElementById("email");
const registrationPassword = document.getElementById("password");
const registrationConfirmPassword = document.getElementById("confirm-password");
const loginEmail = document.getElementById("login-email");
const loginPassword = document.getElementById("login-password");

// Add event listeners to forms
registrationForm.addEventListener("submit", validateRegistrationForm);
loginForm.addEventListener("submit", validateLoginForm);

// Validation functions
function validateRegistrationForm(event) {
  event.preventDefault();
  // Check if email is valid format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(registrationEmail.value)) {
    event.preventDefault();
    alert("Please enter a valid email address.");
    return;
  }

  // Check if password is at least 8 characters long
  if (registrationPassword.value.length < 8) {
    event.preventDefault();
    alert("Password must be at least 8 characters long.");
    return;
  }

  // Check if password and confirm password fields match
  if (registrationPassword.value !== registrationConfirmPassword.value) {
    event.preventDefault();
    alert("Passwords do not match. Please try again.");
    return;
  }
  const email = registrationEmail.value;
  const password = registrationPassword.value
  fetch('http://localhost:5000/register', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: {email},
      password: {password}
    })
  })
  .then(function(response) {
    // Handle the successful login
    alert("Register completed please login to website");
    console.log(response);
  })
  .catch(function(error) {
    // Handle the error
    alert("Hold on we have an issue with our system");
    console.log(error);
  });
  
}
function validateLoginForm(event) {
    // Check if email is valid format
    event.preventDefault();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(loginEmail.value)) {
      event.preventDefault();
      alert("Please enter a valid email address.");
      return;
    }
  
    // Check if password is at least 8 characters long
    if (loginPassword.value.length < 8) {
      event.preventDefault();
      alert("Password must be at least 8 characters long.");
      return;
    }
  
    const email = loginEmail.value;
    const password = loginPassword.value;
    fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: {email},
        password: {password}
      })
    })
    .then(function(response) {
      // Handle the successful login
      if (response.status === 200) {
        // Save the session token to sessionStorage
        response.json().then(function(data) {
          sessionStorage.setItem('sessionToken', data.session_token);
          alert("login is okay")
          // Redirect the user to the secret page
          window.location.href = 'secret';
        });
      } else {
        alert("Password or username is not correct");
      }
      console.log(response);
    })
    .catch(function(error) {
      // Handle the error
      alert("Hold on we have an issue with our system");
      console.log(error);
    });
  }