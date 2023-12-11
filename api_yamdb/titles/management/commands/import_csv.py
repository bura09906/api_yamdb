import csv
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from titles.models import Category, Genre, Title, GenreTitle
from reviews.models import Comment, Review

User = get_user_model()

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

        User.objects.all().delete()
        with open('static/data/users.csv', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )

        Review.objects.all().delete()
        with open('static/data/review.csv', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )

        Comment.objects.all().delete()
        with open('static/data/review.csv', encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review=Review.objects.get(row['review_id']),
                    text=row['text'],
                    pub_date=row['pub_date']
                )