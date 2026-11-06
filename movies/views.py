from django.http import JsonResponse
from .serializers import MovieSerializer, ListQuerySerializer, RatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Movie, Rating

def health(request):
    return JsonResponse({"status": "ok"})

class MovieList(APIView):
    @extend_schema(parameters=[ListQuerySerializer], responses=MovieSerializer(many=True))
    def get(self, request):
        query = ListQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        q = query.validated_data

        items = Movie.objects.order_by("id")
        if "genre" in q:
            items = items.filter(genre__iexact=q["genre"])
        if "year" in q:
            items = items.filter(year=q["year"])
        if "q" in q:
            items = items.filter(title__icontains=q["q"])

        start = q["offset"]
        return Response(MovieSerializer(items[start : start + q["limit"]], many=True).data)

    @extend_schema(request=MovieSerializer, responses={201: MovieSerializer})
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = Movie.objects.create(**serializer.validated_data)
        return Response(MovieSerializer(movie).data, status=201)

def find_movie(movie_id):
    try:
        return Movie.objects.filter(pk=int(movie_id)).first()
    except (ValueError, OverflowError):
        return None

def not_found():
    return Response({"error": "Фильм не найден", "field": "id"}, status=404)\

class MovieMethods(APIView):
    @extend_schema(responses=MovieSerializer)
    def get(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        return Response(MovieSerializer(movie).data)

    @extend_schema(request=MovieSerializer, responses=MovieSerializer)
    def patch(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        serializer = MovieSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(movie, field, value)
        movie.save()
        return Response(MovieSerializer(movie).data)

    @extend_schema(responses={204: None})
    def delete(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        movie.delete()
        return Response(status=204)

class RatingList(APIView):
    def get(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        ratings = movie.ratings.order_by("id")
        return Response(RatingSerializer(ratings, many=True).data)

    def post(self, request, movie_id):
        movie = find_movie(movie_id)
        if movie is None:
            return not_found()
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating = Rating.objects.create(movie=movie, **serializer.validated_data)
        return Response(RatingSerializer(rating).data, status=201)