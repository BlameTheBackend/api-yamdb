# api_yamdb

Проект YaMDb собирает отзывы пользователей на произведения (фильмы, книги, музыку).

## Модели

- **Users** — пользователи (роли: user, moderator, admin)
- **Category** — категории произведений (фильмы, книги, музыка)
- **Genre** — жанры произведений (драма, комедия, рок и т.д.)
- **Title** — произведения (название, год, описание)
- **Review** — отзывы на произведения (оценка 1-10)
- **Comment** — комментарии к отзывам

## API Endpoints

### Категории
- `GET /api/v1/categories/` — список категорий
- `POST /api/v1/categories/` — создать категорию (admin)
- `DELETE /api/v1/categories/{slug}/` — удалить категорию (admin)

### Жанры
- `GET /api/v1/genres/` — список жанров
- `POST /api/v1/genres/` — создать жанр (admin)
- `DELETE /api/v1/genres/{slug}/` — удалить жанр (admin)

### Произведения
- `GET /api/v1/titles/` — список произведений
- `POST /api/v1/titles/` — создать произведение (admin)
- `GET /api/v1/titles/{id}/` — получить произведение
- `PATCH /api/v1/titles/{id}/` — обновить (admin)
- `DELETE /api/v1/titles/{id}/` — удалить (admin)

### Отзывы
- `GET /api/v1/titles/{title_id}/reviews/` — отзывы к произведению
- `POST /api/v1/titles/{title_id}/reviews/` — создать отзыв
- и т.д.

### Комментарии
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/`
- `POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/`
- и т.д.

## Права доступа

- **Аноним** — только чтение (GET)
- **Аутентифицированный пользователь** — чтение, создание отзывов/комментариев, редактирование своего
- **Модератор** — как user + удаление любых отзывов/комментариев
- **Администратор** — полные права на всё

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ThinkLikeHorsie/api-yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```
python -m venv env
. venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python manage.py migrate
```

Создайте суперпользователя:
```
python manage.py createsuperuser
```

Запустить проект:
```
python3 manage.py runserver
```

## Импорт данных

```bash
python manage.py import_csv
```


