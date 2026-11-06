from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)        

    class Meta:
        indexes = [models.Index(fields=["year"], name="movie_year_idx")]

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    viewer = models.CharField(max_length=200)
    score = models.IntegerField()
    review = models.TextField(blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie", "viewer"], name="one_rating_per_viewer")
        ]