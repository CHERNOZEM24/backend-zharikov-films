from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    year = serializers.IntegerField(min_value=1900, max_value=2100)
    genre = serializers.CharField(max_length=100)

class ListQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=1, max_value=100, default=10)
    offset = serializers.IntegerField(min_value=0, default=0)
    genre = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False)
    q = serializers.CharField(required=False)

class RatingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    movie_id = serializers.IntegerField(read_only=True)
    viewer = serializers.CharField(max_length=100)
    score = serializers.IntegerField(min_value=1, max_value=10)
    review = serializers.CharField(required=False, allow_blank=True)