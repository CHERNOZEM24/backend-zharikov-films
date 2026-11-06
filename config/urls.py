from django.contrib import admin
from django.urls import path
from movies.views import health, MovieList, MovieMethods, RatingList, MovieStats
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', health),
    path('api/movies', MovieList.as_view()),
    path('api/movies/<str:movie_id>', MovieMethods.as_view()),
    path("openapi.json", SpectacularJSONAPIView.as_view(), name="schema"),
    path("docs", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/movies/<str:movie_id>/ratings", RatingList.as_view()),
    path("api/movies/stats", MovieStats.as_view()),
path("api/movies/<str:movie_id>", MovieMethods.as_view()),
]
