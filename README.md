Steps to run the project:
1. Clone the project using: "git clone https://github.com/Jinay98/Weather-App-Backend.git"
2. Go to the project directory
3. Create a virtual environment by: "python3 -m venv env"
4. Activate the virtual environment by "source env/bin/activate"
5. Install requirements: "pip3 install -r requirements.txt"
6. Start Django Server by "python3 manage.py runserver"
7. Add Weather API secret key in development.py, staging.py and production.py
8. Add Email Password in development.py, staging.py and production.py
9. Install Redis-Server using https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
10. Start Celery Worker by: "celery worker -A weather_app -Q high_priority,default --loglevel=DEBUG"
11. Check if server is running by testing: http://127.0.0.1:8000/api/server-status/
   