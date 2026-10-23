from django.http import JsonResponse
from .serializers import MovieSerializer, ListQuerySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

def health(request):
    return JsonResponse({"status": "ok"})

movies = {}
next_id = 1

class MovieList(APIView):
    @extend_schema(parameters=[ListQuerySerializer], responses=MovieSerializer(many=True))
    def get(self, request):
        query = ListQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        q = query.validated_data

        items = list(movies.values())
        if "genre" in q:
            items = [m for m in items if m["genre"].lower() == q["genre"].lower()]
        if "year" in q:
            items = [m for m in items if m["year"] == q["year"]]

        start = q["offset"]
        return Response(items[start : start + q["limit"]])

    @extend_schema(request=MovieSerializer, responses={201: MovieSerializer})
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
    @extend_schema(responses=MovieSerializer)
    def get(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        return Response(movie)

    @extend_schema(request=MovieSerializer, responses=MovieSerializer)
    def patch(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        serializer = MovieSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        movie.update(serializer.validated_data)
        return Response(movie)

    @extend_schema(responses={204: None})
    def delete(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        del movies[movie["id"]]
        return Response(status=204)
        