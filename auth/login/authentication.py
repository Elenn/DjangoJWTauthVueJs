import jwt 
from django.conf import settings 
from rest_framework import authentication, exceptions 
from .models import User 

class JWTAuthentication(authentication.BaseAuthentication): 

    def authenticate(self, request):
        
        request.user = None 
        
        auth_header = authentication.get_authorization_header(request).split() 

        if not auth_header:
            return None

        if len(auth_header) == 1: 
            return None

        elif len(auth_header) > 2: 
            return None
 
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8') 

        try:
            #payload = jwt.decode(token, settings.SECRET_KEY)
            payload = jwt.decode(token, 'secret', algorithm=['HS256']) 
            
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token) 