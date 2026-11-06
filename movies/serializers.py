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