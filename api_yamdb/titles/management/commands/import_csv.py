import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Comment, Review
from titles.models import Category, Genre, GenreTitle, Title

User = get_user_model()


class Command(BaseCommand):
    MODELS_DATA_PATH = {
        Category: 'static/data/category.csv',
        Genre: 'static/data/genre.csv',
        Title: 'static/data/titles.csv',
        GenreTitle: 'static/data/genre_title.csv',
        User: 'static/data/users.csv',
        Review: 'static/data/review.csv',
        Comment: 'static/data/comments.csv'
    }

    help = (
        'Imports data from a CSV file into all models.'
        'WARNING old data will be erased!'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--add', action='store_true',
            help='Добавить новые записи к уже существующим'
        )

    def handle(self, *args, **options):
        for model, file_path in self.MODELS_DATA_PATH.items():
            if not options['add']:
                model.objects.all().delete()
            self.import_data(model, file_path)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def import_data(self, model, file_path):
        objects_to_create = []
        try:
            with open(file_path, encoding='utf8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if 'category' in row:
                        category_id = row['category']
                        row['category'] = Category.objects.get(id=category_id)
                    if 'author' in row:
                        author_id = row['author']
                        row['author'] = User.objects.get(id=author_id)
                    obj = model(**row)
                    objects_to_create.append(obj)
            model.objects.bulk_create(objects_to_create)
        except Exception as e:
            raise Exception(
                f'При импорте данных в {model.__name__}'
                f'возникла следующая ошибка: {e}'
            )
