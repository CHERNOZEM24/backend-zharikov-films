import random

from django.core.management.base import BaseCommand

from movies.models import Movie, Rating

GENRES = ["драма", "комедия", "фантастика", "боевик", "триллер", "ужасы",
          "мелодрама", "детектив", "приключения", "мультфильм"]


class Command(BaseCommand):
    help = "Заполняет пустую базу тестовыми данными"

    def handle(self, *args, **options):
        if Movie.objects.exists():
            self.stdout.write("База не пустая, сиды пропущены")
            return

        Movie.objects.bulk_create([
            Movie(title=f"Тестовый фильм {i}", year=random.randint(1950, 2025),
                  genre=random.choice(GENRES))
            for i in range(5000)
        ])

        first = Movie.objects.order_by("id").first()
        Rating.objects.create(movie=first, viewer="Иванов", score=8, review="Отлично")
        self.stdout.write(f"Создано фильмов: {Movie.objects.count()}")