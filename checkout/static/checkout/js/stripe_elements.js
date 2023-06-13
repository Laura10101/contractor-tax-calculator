var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var style = {
    base: {
      color: "#000000",
    }
  };

var card = elements.create('card');
card.mount('#card-element', {style: style});

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
  var errorDiv = document.getElementById('card-errors');
  if (event.error) {
      var html = `
          <span class="icon" role="alert">
              <i class="fas fa-times"></i>
          </span>
          <span>${event.error.message}</span>
      `;
      $(errorDiv).html(html);
  } else {
      errorDiv.textContent = '';
  }
});

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({ 'disabled': true});
  $('#submit-button').attr('disabled', true);

  // Collect details needed for payment method from form 
    let city = $("#town_or_city").val();
    let country = $("#country").val();
    let line1 = $("#street_address1").val();
    let line2 = $("#street_address2").val();
    let postalCode = $("#postcode").val();
    let email = $("#email").val();
    let name = $("#full_name").val();

    // Build data object for Stripe
    let data = {
      "type": "card",
      "card": card,
      "billing_details": {
        "name": name,
        "email": email,
        "address": {
          "city": city,
          "country": "GB",
          "line1": line1,
          "line2": line2,
          "postal_code": postalCode
        }
      }

    }

  // Create payment method in stripe
  // Modified from Stripe's documentation
  // https://stripe.com/docs/js/payment_methods/create_payment_method
  stripe
  .createPaymentMethod(data)
  .then(function(result) {
    // Handle result.error or result.paymentMethod
    paymentMethodId = result.paymentMethod.id;
    $("#payment_method_id").val(paymentMethodId);

    // Submit the form
    $("#payment-form").submit();
  });
});