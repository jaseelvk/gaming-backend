from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    if user.userprofile.role == 'admin':
        
        refresh.set_exp(lifetime=timedelta(days=30))  
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
