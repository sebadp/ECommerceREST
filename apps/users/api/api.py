from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer

# class UserAPIView(APIView):

#     def get(self, request):
#         users = User.objects.all()
#         users_serializer = UserSerializer(users, many=True)
#         return Response(users_serializer.data)


'''
La siguiente vista nos lista todos los usuarios, con el método GET. 
También nos permite crear un usuario nuevo con el método POST.
'''
@api_view(['GET', 'POST'])
def user_api_view(request, ):
    
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user_serializer = UserSerializer( data = request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        # Si hay un error se auto genera un atributo 'errors'
        return Response(user_serializer.errors)

"""
La siguiente función nos devuelve:
GET: nos trae un usuario en particular. Le indicamos cuál en la ruta. 
Para esto hay que configurarlo en urls.py y luego lo tomamos como argumento pk, que viene junto al request.
PUT: le pasamos el usuario en la db y la data que ingresa el usuario
para que lo compare y actualize lo diferente

"""
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):

    if request.method == 'GET':
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    elif request.method == 'PUT':
        user = User.objects.filter(id=pk).first()
        # en la siguiente línea: le pasamos el usuario en la db y la data que ingresa el usuario
        # para que lo compare y actualize lo diferente
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        return Response(user_serializer.errors)

    elif request.method == 'DELETE':
        user = User.objects.filter(id=pk).first()
        user.delete()
        return Response('Eliminado')
