from rest_framework.views import APIView
from rest_framework.response import Response


class HelloAPIView(APIView):
    '''
    Test API view
    '''

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