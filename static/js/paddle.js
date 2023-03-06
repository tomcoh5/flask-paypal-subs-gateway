// Get the subscription form element
const subscriptionForm = document.getElementById('subscription-form');

// Add an event listener to the subscription form
subscriptionForm.addEventListener('submit', async (event) => {
    // Prevent the form from submitting
    event.preventDefault();

    // Get the subscription details from the form
    const planId = subscriptionForm.elements['plan_id'].value;
    const email = subscriptionForm.elements['email'].value;

    // Send the subscription details to the server
    const response = await fetch('/create_subscription', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'plan_id': planId,
            'email': email
        })
    });

    // Get the subscription ID from the server response
    const data = await response.json();
    const subscriptionId = data.subscription_id;

    // Redirect the user to the Paddle checkout page
    Paddle.Checkout.open({
        product: planId,
        email: email,
        passthrough: email,
        subscription_id: subscriptionId,
        successCallback: function(data) {
            // Handle the successful checkout
            alert('Thank you for subscribing!');
        },
        closeCallback: function() {
            // Handle the checkout window being closed
            alert('Checkout window closed.');
        }
    });
});
