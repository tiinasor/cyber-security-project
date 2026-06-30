# Cyber Security Project

The app is a simple polls application where logged-in users can vote, search polls, and view results. It is based on the [Django tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/). It intentionally contains five security flaws from the [OWASP Top 10 2021](https://owasp.org/Top10/2021/) list, along with their fixes commented out in the code.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project folder:
   ```
   cd djangotutorial
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Create a superuser (admin):
   ```
   python manage.py createsuperuser
   ```
6. Start the server:
   ```
   python manage.py runserver
   ```
7. Open http://localhost:8000/polls/ in your browser
