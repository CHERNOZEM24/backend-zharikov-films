from django.contrib import admin
from django.urls import path
from movies.views import health, MovieList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health),
    path('api/movies', MovieList.as_view()),
]
