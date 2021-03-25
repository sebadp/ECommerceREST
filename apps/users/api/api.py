from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, TestUserSerializer

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
    
    # List
    if request.method == 'GET':
        
        # queryset
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)

        # hacemos un diccionario para pasarlo como data para hacer un usuario de prueba
        test_data={
            'name': "seba",
            'email': 'developer@gmail.com',
        }
        # serializamos la info con la clase que creamos en serializers
        test_user = TestUserSerializer(data=test_data)

        # si pasa la validación imprimimos un mensaje.>> Se guarda la data en validated_data
        # pero si no lo pasa, crea un diccionario llamado "errors" que luego lo podemos imprimir.
        if test_user.is_valid():
            user_instance = test_user.save()
            print("Pasó las validaciones")
        else :
            print(test_user.errors)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    # Create
    elif request.method == 'POST':

        # queryset
        user_serializer = UserSerializer( data = request.data)

        # validation
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'El usuario ha sido creado con éxito.'}, status=status.HTTP_201_CREATED)

        # Si hay un error se auto genera un atributo 'errors' en el serializer, como en los forms.
        return Response(user_serializer.errors)

"""
La siguiente función nos devuelve:
GET: nos trae un usuario en particular. Le indicamos cuál en la ruta. 
Para esto hay que configurarlo en urls.py y luego lo tomamos como argumento pk, que viene junto al request.
PUT: le pasamos el usuario en la db y la data que ingresa el usuario
para que lo compare y actualize lo diferente
DELETE: 
"""
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request, pk=None):
    
    # queryset
    user = User.objects.filter(id=pk).first()

    # valitation
    if user:
        # retrive
        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        # update
        elif request.method == 'PUT':

            """
            en la siguiente línea: le pasamos el usuario en la db y la data que ingresa el usuario
            para que lo compare y actualize lo diferente
            """

            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'El usuario ha sido eliminado con éxito.'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un usuario con estos datos.'}, status=status.HTTP_400_BAD_REQUEST)