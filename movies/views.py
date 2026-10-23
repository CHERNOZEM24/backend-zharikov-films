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