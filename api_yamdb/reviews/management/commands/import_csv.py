import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
# from users.models import User
from reviews.models import Review, Comment


class Command(BaseCommand):
    help = 'Import data from csv files'

    def handle(self, *args, **options):
        with open('static/data/category.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write('Categories imported')

        with open('static/data/genre.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
        self.stdout.write('Genres imported')

        with open('static/data/titles.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category']
                )
        self.stdout.write('Titles imported')

        with open('static/data/genre_title.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
        self.stdout.write('Genre-Title relations imported')

        # with open('static/data/users.csv', 'r', encoding='utf-8') as f:
        #     reader = csv.DictReader(f)
        #     for row in reader:
        #         User.objects.get_or_create(
        #             id=row['id'],
        #             username=row['username'],
        #             email=row['email'],
        #             role=row['role'],
        #             bio=row['bio'],
        #             first_name=row['first_name'],
        #             last_name=row['last_name']
        #         )
        # self.stdout.write('Users imported')

        with open('static/data/review.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    author_id=row['author'],
                    text=row['text'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
        self.stdout.write('Reviews imported')

        with open('static/data/comments.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Comment.objects.get_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    author_id=row['author'],
                    text=row['text'],
                    pub_date=row['pub_date']
                )
        self.stdout.write('Comments imported')
