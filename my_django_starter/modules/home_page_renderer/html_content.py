# my_django_starter/html_content.py

HOME_HTML = """{% extends 'base.html' %}
{% block title %}Django - Home Page {% endblock %}
{% block content %}
<!-- Inject favicon dynamically -->
<script>
    (function() {
        const link = document.createElement('link');
        link.rel = 'icon';
        link.type = 'image/svg+xml';
        link.href = 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg';
        document.head.appendChild(link);
    })();
</script>

<div class="min-h-screen bg-gradient-to-r from-green-900 via-emerald-800 to-lime-700 flex flex-col items-center justify-center text-white">
    <h1 class="text-5xl font-bold mb-4 animate-pulse">Welcome to Your Django Project!</h1>
    <p class="text-xl mb-8">Start with my-django-starter for rapid development.</p>
    <div class="space-x-4">
        {% for app in apps %}
        <a href="{% url app|add:'_home' %}" class="bg-emerald-600 text-white px-6 py-3 rounded-full font-semibold hover:bg-emerald-500 transition">
            Visit {{ app|capfirst }}
        </a>
        {% endfor %}
    </div>
</div>
{% endblock %}
"""



VIEWS_CONTENT = """# views.py
from django.shortcuts import render

def home_view(request):
    return render(request, 'home/home.html')

"""

URLS_CONTENT = """# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
]

"""

