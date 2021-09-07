from .models import Zmogus
from django.conf import settings

# requires to define two functions authenticate and get_user

#class YourAuth:  

 #   def authenticate(self, request, username=None):
 #       try:
 #           user = Zmogus.objects.get(vardas=username)
 #           return user
 #       except Zmogus.DoesNotExist:
 #           return None
 #       
 #   def get_user(self, user_id):
 #       try:
 #           return Zmogus.objects.get(id=user_id)
 #       except Zmogus.DoesNotExist:
 #           return None

    