# Simple JWT Authentication pour MSP
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

#conexion et génération tokens
@extend_schema(
    summary="connexion utilisateur",
    description="authentifie un user et retourne les tokens JWT access et refresh",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'user1'},
                'password': {'type': 'string', 'example': 'azerty123'}
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: OpenApiResponse(
            description="connexion réussie, tokens générés",
            examples=[
                OpenApiExample(
                    'success',
                    value={'access': 'aaaaaaaaa...', 'refresh': 'bbbbbbb...'}
                )
            ]
        ),
        400: OpenApiResponse(description="username ou password manquant"),
    },
    tags=['Authentication']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'need username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        else:
            return Response({'error': 'invalide'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Utilisateur introuvable'}, status=status.HTTP_401_UNAUTHORIZED)

# creation d'un nouvel utilisateur
@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    if not username or not password:
        return Response({'error': 'need username and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'user already exist'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'succès',
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }, status=status.HTTP_201_CREATED)

# profil utilisateur
@extend_schema(exclude=True)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        }
    })
