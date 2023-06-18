from .models import Subscription

# Create service method to create subscription 
def create_subscription(user_id, subscription_option_id):
    # Load the subscription option
    subscription_option = SubscriptionOption.objects.get(pk=subscription_option_id)
    # Create new subscription in the database 
    new_subscription = Subscription.objects.create(user_id=user_id, subscription_option=subscription_option)
    # Return ID of newly created jurisdiction
    return new_subscription.id

# Create service method to check subscription 
def check_subscription(user_id):
    # Get the subscription from the database for the user ID 
    subscriptions = Subscription.objects.filter(user_id=user_id)
    # Return an error if more than one subscription 
    if subscriptions.count() > 1:
        raise Exception ("More than one subscription found for user")
    # Return false if no subscription for that user ID
    if subscriptions.count() <= 0:
        return False
    # If subscription, call is_active function and return result
    return subscriptions.first().is_active()

# Create service method to update subscription 
def update_subscription(id, subscription_option_id):
    # Load the subscription option
    subscription_option = SubscriptionOption.objects.get(pk=subscription_option_id)
    # Get subscription from database 
    # Patch start date
    # Patch subscription months 
    subscription = Subscription.objects.get(pk=id).update(
        start_date = date.today(),
        subscription_option = subscription_option
        )

# Load all subscription options
def get_subscription_options():
    return SubscriptionObject.objects.all()