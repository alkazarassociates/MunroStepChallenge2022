# From https://www.javatpoint.com/django-user-registration-with-email-confirmation
from django.contrib.auth.tokens import PasswordResetTokenGenerator  
from django.utils.crypto import salted_hmac

class TokenGenerator(PasswordResetTokenGenerator):  
    def _make_hash_value(self, user, timestamp):
        print(f"Make Hash {user.pk} {timestamp} {user.is_active}")
        ret = (  
            str(user.pk) + str(timestamp) +  
            str(user.is_active)  
        )  
        signature = salted_hmac(self.key_salt, ret, secret=self.secret, algorithm=self.algorithm)
        print(signature)
        return ret
    
account_activation_token = TokenGenerator() 