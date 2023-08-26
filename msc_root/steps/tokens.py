# From https://www.javatpoint.com/django-user-registration-with-email-confirmation
from django.contrib.auth.tokens import PasswordResetTokenGenerator  

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):
        print(f"Make Hash {user.pk} {timestamp} {user.is_active}")
        return (  
            str(user.pk) + str(timestamp) +  
            str(user.is_active)  
        )  
account_activation_token = TokenGenerator() 