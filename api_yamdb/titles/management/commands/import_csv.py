import csv
from typing import Any
from django.core.management.base import BaseCommand
from titles.models import Category, Genre, Title, GenreTitle



class Command(BaseCommand):
    help = 'Imports data from a CSV file into all models. WARNING old data will be erased!'

    def handle(self, *args, **options):
        self.import_data()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def import_data(self):
        Category.objects.all().delete()
        with open('static/data/category.csv', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

        Genre.objects.all().delete()
        with open('static/data/genre.csv', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

        Title.objects.all().delete()
        with open('static/data/titles.csv', encoding="utf8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category'])
                )

        GenreTitle.objects.all().delete()
        with open('static/data/genre_title.csv', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                GenreTitle.objects.create(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    genre=Genre.objects.get(id=row['genre_id']),
                )