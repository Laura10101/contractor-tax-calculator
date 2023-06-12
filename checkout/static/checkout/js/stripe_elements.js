var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var stripe_public_key = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var style = {
    base: {
      color: "#000000",
    }
  };

var card = elements.create('card');
card.mount('#card-element', {style: style});