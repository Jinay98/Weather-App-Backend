from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def server_status(request):
    return Response({"message": "The server is up and running!"}, status=status.HTTP_200_OK)
