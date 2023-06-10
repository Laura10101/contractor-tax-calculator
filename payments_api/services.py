def create_payment(subscription_id, requested_subscription_months, subtotal, currency):
    pass

def confirm_payment(id, billing_street_1, billing_street_2, town_or_city, county, country, postcode, 
    card_number, expiry_date, ccv2):
    pass

def complete_payment(stripe_pid):
    pass

def fail_payment(stripe_pid, reason):
    pass