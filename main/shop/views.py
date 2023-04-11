from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import *
from .serializers import *
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth import authenticate


@api_view(['POST'])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return JsonResponse({
            'body': {
                'user_token': token.key
            }
        }, status=201)
    else:
        return JsonResponse({
            'error': {
                'code': 401,
                'message': 'Authentication failed',
                'errors': serializer.errors
            }
        }, status=401)


@api_view(['POST'])
def sign_in(request):
    serializer = SignInSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if not user:
            return JsonResponse({
                'error': {
                    'code': 401,
                    'message': 'Authentication failed',
                    'errors': serializer.errors
                }
            }, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'body': {
                'user_token': token.key
            }
        }, status=200)
    else:
        return JsonResponse({
            'error': {
                'code': 422,
                'message': 'Validation failed',
                'errors': serializer.errors
            }
        }, status=422)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sign_out(request):
    request.user.auth_token.delete()
    return JsonResponse({
        'body': {
            'message': 'logout'
        }
    }, status=200)


@permission_classes([AllowAny])
@api_view(["GET"])
def product_view(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({
            'body': serializer.data
        }, status=200)


@permission_classes([IsAdminUser])
@api_view(["POST"])
def product_add(request):
    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'body': {
                    'id': serializer.data['id'],
                    'message': 'Product added'
                }
            }, status=201)
        else:
            return JsonResponse({
                'error': {
                    'code': 422,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }
            }, status=422)


@permission_classes([IsAdminUser])
@api_view(["GET", "PATCH", "DELETE"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return JsonResponse({"error": {"code": 404, "message": 'Not found'}}, status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse({'body': serializer.data}, status=200)

    if request.method == "PATCH":
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"data": serializer.data}, status=200)
        else:
            return JsonResponse({
                'error': {
                    'code': 422,
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }
            }, status=422)

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({'data': {'message': 'product removed'}}, status=200)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def cart_view(request):
    if request.method == 'GET':
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart, many=True)
        return JsonResponse({'body': serializer.data}, status=200)


@permission_classes([IsAuthenticated])
@api_view(["POST", "DELETE"])
def add_delete_in_cart(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return JsonResponse({"error": {"code": 404, "message": 'Not found'}}, status=404)

    if request.method == 'POST':
        cart = Cart.objects.create(user=request.user)
        cart.products.add(product)
        return JsonResponse({"body": {"message": "Product added to cart"}}, status=200)

    if request.method == 'DELETE':
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        return JsonResponse({"body": {"message": "Product removed from cart"}}, status=200)
