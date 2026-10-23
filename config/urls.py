from django.contrib import admin
from django.urls import path
from movies.views import health, MovieList, MovieMethods

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health),
    path('api/movies', MovieList.as_view()),
    path('api/movies/<str:movie_id>', MovieMethods.as_view()),
]
