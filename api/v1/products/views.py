from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from product.models import Product, UserProfile, Wishlist
from .serializers import TaskSerializer, ProductSerializer, ProductDetailSerializer, WishlistSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(["GET"])
@permission_classes([AllowAny])
def products(request):
    instances = Product.objects.filter(is_deleted=False)
    serializer = ProductSerializer(instances, many=True, context={"request": request})
    response_data = {
        "status_code": 6000,
        "data": serializer.data
    }
    return Response(response_data)

@api_view(["GET"])
@permission_classes([AllowAny])
def product(request, pk):
    try:
        instance = Product.objects.get(pk=pk, is_deleted=False)
        serializer = ProductDetailSerializer(instance, context={"request": request})
        response_data = {
            "status_code": 6000,
            "data": serializer.data
        }
        return Response(response_data)
    except Product.DoesNotExist:
        response_data = {
            "status_code": 6001,
            "message": "Product not found"
        }
        return Response(response_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    logger.info('Request Headers: %s', request.headers)
    logger.info('Request Data: %s', request.data)

    if not request.user.is_authenticated:
        logger.error('User not authenticated')
        return Response({
            "status_code": 6001,
            "message": "Unauthorized"
        }, status=401)

    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'admin':
            logger.error('User role is not admin')
            return Response({
                "status_code": 6001,
                "message": "Only admins can add products"
            }, status=403)
    except UserProfile.DoesNotExist:
        logger.error('User profile does not exist')
        return Response({
            "status_code": 6001,
            "message": "User profile does not exist"
        }, status=400)

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        try:
            product = serializer.save(created_by=request.user)
            response_data = {
                "status_code": 6000,
                "message": "Product Added",
                "data": TaskSerializer(product).data
            }
            logger.info('Product added successfully')
            return Response(response_data)
        except serializers.ValidationError as e:
            logger.error('Validation error: %s', e)
            return Response({
                "status_code": 6001,
                "message": "Validation error",
                "errors": e.detail,
            }, status=400)
    else:
        logger.error('Serializer errors: %s', serializer.errors)
        response_data = {
            "status_code": 6001,
            "message": "Oops..Something went wrong...!",
            "data": serializer.errors
        }
        return Response(response_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request, pk):
    logger.info('Received request to add product to wishlist')
    auth_header = request.headers.get("Authorization")
    logger.info(f'Authorization Header: {auth_header}')
    
    if auth_header:
        token = auth_header.split(' ')[1]
        logger.info(f'Token: {token}')
    
    logger.info(f'User: {request.user}, Is authenticated: {request.user.is_authenticated}')
    
    if not request.user.is_authenticated:
        return Response({"message": "User not authenticated"}, status=401)
    
    try:
        product = Product.objects.get(pk=pk, is_deleted=False)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if created:
            response_data = {
                "status_code": 6000,
                "message": "Product added to wishlist"
            }
        else:
            response_data = {
                "status_code": 6001,
                "message": "Product is already in wishlist"
            }
        return Response(response_data)
    except Product.DoesNotExist:
        response_data = {
            "status_code": 6001,
            "message": "Product not found"
        }
        return Response(response_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    serializer = WishlistSerializer(wishlist_items, many=True, context={"request": request})
    response_data = {
        "status_code": 6000,
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, pk):
    logger.info('Received request to remove product from wishlist')
    auth_header = request.headers.get("Authorization")
    logger.info(f'Authorization Header: {auth_header}')
    
    if auth_header:
        token = auth_header.split(' ')[1]
        logger.info(f'Token: {token}')
    
    logger.info(f'User: {request.user}, Is authenticated: {request.user.is_authenticated}')
    
    if not request.user.is_authenticated:
        return Response({"message": "User not authenticated"}, status=401)
    
    try:
        product = Product.objects.get(pk=pk, is_deleted=False)
        wishlist = Wishlist.objects.filter(user=request.user, product=product)
        if wishlist.exists():
            wishlist.delete()
            response_data = {
                "status_code": 6000,
                "message": "Product removed from wishlist"
            }
        else:
            response_data = {
                "status_code": 6001,
                "message": "Product is not in wishlist"
            }
        return Response(response_data)
    except Product.DoesNotExist:
        response_data = {
            "status_code": 6001,
            "message": "Product not found"
        }
        return Response(response_data)
