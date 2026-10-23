from django.http import JsonResponse
from .serializers import MovieSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

def health(request):
    return JsonResponse({"status": "ok"})

movies = {}
next_id = 1

class MovieList(APIView):
    def get(self, request):
        return Response(list(movies.values()))

    def post(self, request):
        global next_id
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = {"id": next_id, **serializer.validated_data}
        movies[next_id] = movie
        next_id += 1
        return Response(movie, status=201)

def find_movie(movie_id):
    try:
        return movies.get(int(movie_id))
    except ValueError:
        return None

def not_found():
    return Response({"error": "Фильм не найден", "field": "id"}, status=404)\

class MovieMethods(APIView):
    def get(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        return Response(movie)

    def patch(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        serializer = MovieSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        movie.update(serializer.validated_data)
        return Response(movie)

    def delete(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        del movies[movie["id"]]
        return Response(status=204)
        