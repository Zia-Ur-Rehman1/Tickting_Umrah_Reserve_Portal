Python 3.12
Django 5.0
pipenv shell

python -m pip install django
djando-admin startproject ticket_management .
python manage.py startapp ticket

python -m pip install django-tailwind
In settings.py installed app add tailwind

python -m pip install 'django-tailwind[reload]'
In settings.py installed app add django_browser_reload
Also add
Middle Ware
"django_browser_reload.middleware.BrowserReloadMiddleware",
Add in urls
path("__reload__/", include("django_browser_reload.urls")),
from django.urls import path, include


python manage.py tailwind init
python manage.py tailwind install
The command will ask for the name fo Tailwind app by default they keep it theme
After that add  'theme', in Installed apps
in Settings.py add 
INTERNAL_IPS = [
    "127.0.0.1",
]
After tailwind init if a base file is created in the theme/templates or else create a new one and add the following

{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
	<head>
    <title>Django Tailwind</title>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta http-equiv="X-UA-Compatible" content="ie=edge">
		{% tailwind_css %}
	</head>

	<body class="">
		{% block content %}{% endblock %}
	</body>
</html>

Now we need to add tailwind elements like popup modal and dropdown and alerts etc..
 npm install -D tailwindcss postcss autoprefixer\nnpx tailwindcss init -p
 npm install tw-elements
 source: https://tw-elements.com/docs/standard/components/alerts/

 in settings.py 
 STATICFILES_DIRS = [
  BASE_DIR / "theme/static",
  BASE_DIR.parent / "Husnain_Travels/node_modules",
]


in base.html before closing the body tag add
	<script
	src="{% static 'tw-elements/dist/js/tw-elements.umd.min.js' %}"
	type="text/javascript"></script>