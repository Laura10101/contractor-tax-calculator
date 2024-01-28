var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements({ clientSecret: client_secret });

var style = {
    base: {
      color: "#000000",
    }
  };

const address = elements.create('address', { mode: 'billing' });
const card = elements.create('card');

address.mount('#address-element');
card.mount('#card-element', {style: style});

function elementsAreValid()  {
  let addressELementDiv = document.getElementById("address-element");
  let cardELementDiv = document.getElementById("card-element");

  return addressELementDiv.classList.contains("StripeElement") && cardELementDiv.classList.contains("StripeElement--complete");
};

// Enable/disable the submit button
address.addEventListener('change', function (event) {
  let submit = document.getElementById("submit-button");
  if (elementsAreValid()) {
    submit.disabled = false;
  } else {
    submit.disabled = true;
  }
});

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
      let submit = document.getElementById("submit-button");
      errorDiv.textContent = '';
      if (elementsAreValid()) {
        submit.disabled = false;
      } else {
        submit.disabled = true;
      }
  }
});

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({ 'disabled': true});
  $('#submit-button').attr('disabled', true);

    // Build data object for Stripe
    let data = {
      elements
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