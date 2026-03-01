import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


DATA_DIR = Path('static/data')
CSV_FILES = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': 'many_to_many',
    'users.csv': User,
    'review.csv': Review,
    'comments.csv': Comment,
}


class Command(BaseCommand):
    """Команда для импорта данных из CSV файлов."""

    help = 'Импорт данных из CSV файлов в базу данных'

    def add_arguments(self, parser):
        """Добавление аргументов командной строки."""
        parser.add_argument(
            '--data-dir',
            type=str,
            default='static/data',
            help='Директория с CSV файлами (по умолчанию: static/data)'
        )

    def _import_model_data(self, filename, model):
        """Импорт данных для обычной модели."""
        filepath = DATA_DIR / filename
        if not filepath.exists():
            self.stderr.write(f'Файл не найден: {filepath}')
            return

        foreign_keys = {
            Title: {'category': 'category_id'},
            Review: {'author': 'author_id', 'title': 'title_id'},
            Comment: {'author': 'author_id', 'review': 'review_id'},
        }

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                data = row.copy()

                if model in foreign_keys:
                    for field, fk_field in foreign_keys[model].items():
                        if field in data:
                            data[fk_field] = data.pop(field)

                _, created = model.objects.get_or_create(**data)
                if created:
                    count += 1

            self.stdout.write(f'{filename}: импортировано {count} записей')

    def _import_genre_title(self, filename):
        """Специальный импорт для связи многие-ко-многим."""
        filepath = DATA_DIR / filename
        if not filepath.exists():
            self.stderr.write(f'Файл не найден: {filepath}')
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    title.genre.add(genre)
                    count += 1
                except (Title.DoesNotExist, Genre.DoesNotExist) as e:
                    self.stderr.write(
                        f'Ошибка: {e} в строке {row}'
                    )
            self.stdout.write(
                f'{filename}: создано {count} связей Title-Genre'
            )

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Основной обработчик команды.
        Использует транзакцию для отката при ошибках.
        """
        global DATA_DIR
        DATA_DIR = Path(options['data_dir'])

        self.stdout.write('Начало импорта данных...')

        import_order = [
            'category.csv',
            'genre.csv',
            'titles.csv',
            'genre_title.csv',
            'users.csv',
            'review.csv',
            'comments.csv',
        ]

        for filename in import_order:
            model = CSV_FILES.get(filename)
            if filename == 'genre_title.csv':
                self._import_genre_title(filename)
            elif model:
                self._import_model_data(filename, model)
            else:
                self.stderr.write(f'Неизвестный файл: {filename}')

        self.stdout.write(self.style.SUCCESS('Импорт успешно завершен!'))
