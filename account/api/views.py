from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.api.tasks import email_weather_report
from account.models import AppUser
from account.serializers.UserSerializer import UserSerializer
from account.serializers.WeatherDataSerializer import WeatherDataSerializer
from cache.weathercache import WeatherCache


@api_view(['POST'])
def login(request):
    try:
        data = request.data
        phone_number = data.get("phone_number", None)
        password = data.get("password", None)
        response = {}
        if AppUser.objects.filter(phone_number=phone_number).exists():
            user = AppUser.objects.get(phone_number=phone_number)
            if user.check_password(password):
                try:
                    token = user.auth_token.key
                except:
                    token = Token.objects.create(user=user)
                user.is_active = True
                user.save()
                response["token"] = token
                response["message"] = "User has successfully logged in"
                return Response(response, status=status.HTTP_200_OK)
            else:
                response["token"] = None
                response["message"] = "Entered password is incorrect"
                return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            response["token"] = None
            response["message"] = "No such user exists with the given phone number"
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def register(request):
    try:
        data = request.data
        serializer = UserSerializer(data=data)
        response = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            response['token'] = token
            response["message"] = "User created successfully"
            response["user_details"] = serializer.data
            return Response(response, status.HTTP_201_CREATED)
        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    try:
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "User has successfully logged out"})
    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_weather_data(request):
    try:
        weatherCache = WeatherCache()
        data = weatherCache.get_configuration()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(data, request)
        serializer = WeatherDataSerializer(result_page, many=True)
        result = paginator.get_paginated_response(serializer.data)
        response = result.data
        return Response(response)
    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def send_email(request):
    try:
        email_list = request.data.get("email_list")
        valid_email_list = []
        for email in email_list:
            try:
                validate_email(email)
                valid_email_list.append(email)
            except ValidationError:
                continue
        email_weather_report.apply_async(bind=True, args=[valid_email_list], queue="default", routing_key='default',
                                         max_retries=5)
        return Response({"message": "All Emails will be sent in sometime"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
