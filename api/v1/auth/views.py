# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from product.models import UserProfile
from .tokens import get_tokens_for_user
import logging

logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'user')  

    if not username or not email or not password or not role:
        logger.error('All fields are required')
        return Response({
            "status_code": 6002,
            "data": "All fields are required"
        }, status=400)

    if User.objects.filter(username=username).exists():
        logger.error(f'Username {username} already exists')
        return Response({
            "status_code": 6001,
            "data": "Ops... This account already exists..."
        }, status=400)

    if User.objects.filter(email=email).exists():
        logger.error(f'Email {email} already exists')
        return Response({
            "status_code": 6001,
            "data": "Ops... This email is already registered..."
        }, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email
    )
    
    UserProfile.objects.create(user=user, role=role)  
    logger.info(f'UserProfile created for user {username} with role {role}')

    
    tokens = get_tokens_for_user(user)

    response_data = {
        "status_code": 6000,
        "data": tokens,
        "role": role,
        "message": "Congrats...Account created successfully"
    }

    return Response(response_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            "status_code": 6002,
            "data": "All fields are required"
        }, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        tokens = get_tokens_for_user(user)
        user_profile = UserProfile.objects.get(user=user)
        response_data = {
            "status_code": 6000,
            "data": tokens,
            "role": user_profile.role,
            "message": "Login successful"
        }
    else:
        response_data = {
            "status_code": 6001,
            "data": "Invalid credentials"
        }

    return Response(response_data)
