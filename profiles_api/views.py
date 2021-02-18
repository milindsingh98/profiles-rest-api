from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

class HelloAPIView(APIView):
    '''
    Test API view
    '''

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        '''
        Returns a list of APIView Features
        '''
        an_apiview = [
            'Uses HTTP methods as fucntion (get, post, patch, put, delete',
            'Is similar to a traditional Django view',
            'Gives you the most control over application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message' : 'Hello!', 'an_apiview' : an_apiview})

    def post(self, request):
        '''
        Create a helloe request with our name
        '''

        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'

            return Response({'message' : message})

        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                ) 

    def put(self, request, pk= None):
        '''
        handling updating an object
        '''
        return Response({'method': 'PUT'})

    def patch(self, request, pk= None):
        '''
        Handle a partial update of an object
        '''
        return Response({'method':'PATCH'})

    def delete(self, request, pk = None):
        '''
        Delete the object 
        '''
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    '''
    Test API Viewset
    '''
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        '''
        Return a hello message
        '''
        a_viewset = [
            'User actions (list, create, retrieve, update, partiaql_update',
            'Automatically maps to URLs using routers',
            'Provies more functionality with less code',
        ]

        return Response({'message' : 'Hello!' , 'a_viewset' : a_viewset})

    def create(self, request):
        '''
        create a new hello message
        '''
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self,request, pk = None):
        '''
        Handle getting an object by ID
        '''
        return Response({'http_method' : 'GET'})

    def update(self, request, pk=None):
        '''
        Handle updating an obejct
        '''
        return Response({'http_method' :'PUT'})

    def partial_update(self, request, pk = None):
        '''
        Handle updating part of an object
        '''
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        '''
        Handle removing an object
        '''
        return Response({'http_method' : 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    '''
    Handle creating and updating profiles
    '''
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name' , 'email',)

class UserLoginApiView(ObtainAuthToken):
    '''
    handle creating user authentication tokens
    '''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''
    Handlles creating, reading and updating profile feed itens
    '''
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        '''
        sets the user profile to the loggged in user
        '''
        serializer.save(user_profile=self.request.user)