from django.urls import path

from account.api.views import login, register, logout, get_weather_data, send_email

app_name = "account"
urlpatterns = [
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('register', register, name="register"),
    path('weather-data', get_weather_data, name="get_weather_data"),
    path('send-email', send_email, name="send_email"),

]
