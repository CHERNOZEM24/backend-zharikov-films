from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    year = serializers.IntegerField(min_value=1900, max_value=2100)
    genre = serializers.CharField(max_length=100)