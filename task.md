# Backend - Developer - Тестовое Задание

## Описание

Необходимо разработать дополнительный функционал для библиотеки.

В нашу библиотеку раз в месяц приходят большие партии новых книг (от 1000 до 10000).
Необходимо добавить возможность заносить вновь прибывшие книги в базу.
Нужно учитывать что книги могут повторяться,
в таком случае необходимо учитывать количество экземпляров этой книги.

Так же нужна возможность смотреть статистику по имеющимся книгам, а именно:
топ N книг по количеству экземпляров, количество книг у каждого автора,
количество книг по каждому автору.

## Endpoints:
1. `GET /api/books/copies?top=N` - топ N книг по количеству экземпляров
2. `GET /api/authors/{author_id}/stat` - количество книг у автора
3. `GET /api/authors/stat?page=N&page_count=M` - количество книг по каждому автору
4. `POST /api/books/delivery` - занести в базу книги

## Примечания 

- Считать что основной CRUD функционал уже реализован
(но будет приветствоваться его реализация)
- Поставка новых книг - это файл `json` в котором массив объектов книг
- Объект `book` обязательно имеет поля:
  + `count` - количество экземпляров;
  + `title` - название книги;
  + `authors` - список объектов авторов;
  + и другие поля по усмотрению разработчика.
- Объект `author` обязательно имеет поля:
  + `title` - имя автора
  + и другие поля по усмотрению разработчика.
- У книги может быть много авторов, а у автора много книг
- Добавить пагинацию, где это необходимо
- Настроить валидацию get и post параметров, где это необходимо
- Дублей книг или авторов не должно быть в базе 
(настроить индексы уникальности)

## Модели

Минимально необходимо реализовать 2 модели "авторы" и "книги"

## Будет плюсом:
- Реализация дополнительных моделей, например: "поставки", "жанры"
- Покрытие тестами всех endpoint `pytest` (`unittest`)<sup>[1](#choose)</sup>
- Логирование 
- Упаĸовĸа в `Docker`
- Использование миграций (для `django` это обязательно)
- Автоматическое документирование `api` через `Swagger`

## Доступный стек технологий

Для реализации предлагается 1 набора технологий на выбор

2. Django  + Django ORM + DRF + Postgres





[
    {
        "title": "Книга 1",
        "authors": [ 
            "Петр Петров",   
            "Иван Иванов"
            
        ]
    },
    {
        "title": "Книга 2",
        "authors": [
            "Сергей Сергеев",
            "Анна Андреева"
        ]
    },
    {
        "title": "Книга 3",
        "authors": [
            "Михаил Михайлов",
            "Ольга Орлова"
        ]
    },
    {
        "title": "Книга 1",
        "authors": [
            "Иван Иванов",
            "Петр Петров"
        ]
    },
    {
        "title": "Книга 2",
        "authors": [
            "Дмитрий Дмитриев",
            "Екатерина Егорова"
        ]
    },
    {
        "title": "Книга 4",
        "authors": [
            "Алексей Алексеев",
            "Татьяна Тимофеева"
        ]
    }
]