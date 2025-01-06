import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()
import pytest
from rest_framework import status
from main.models import Author, Book
from main.serializers import AuthorSerializerList, BookSerializer
from rest_framework.test import APIClient


@pytest.fixture
def apiclient():
    return APIClient()

@pytest.fixture
def create_authors(db):
    authors = [Author(name=f"Автор {i}") for i in range(4)]
    Author.objects.bulk_create(authors)
    yield authors

@pytest.fixture
def create_books(db):
    authors = [Author(name=f"Автор {i}") for i in range(4)]
    Author.objects.bulk_create(authors)

    books = [Book(title=f"Книга {i}", count=i) for i in range(1, 6)]
    Book.objects.bulk_create(books)

    books[0].authors.add(*authors[:3])
    books[1].authors.add(authors[0], authors[3])
    books[2].authors.add(*authors)
    books[3].authors.add(authors[1])
    books[4].authors.add(authors[0])

    yield books

@pytest.mark.django_db
def test_get_author_stat(apiclient, create_authors):
    response = apiclient.get("/api/authors/stat/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == Author.objects.count()
    for item in response.data['results']:
        assert "books_count" in item

@pytest.mark.django_db
def test_get_author_stat_id(apiclient, create_authors):
    author = Author.objects.first()
    response = apiclient.get(f"/api/authors/{author.id}/stat/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == author.id
    assert "books_count" in response.data


@pytest.mark.django_db
def test_get_top_copies(apiclient, create_books):
    response = apiclient.get("/api/books/copies/?top=2")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    for book in response.data['results']:
        assert "count" in book

@pytest.mark.django_db
def test_delivery_books(apiclient):
    new_book_data = {
        "title": "Новая книга",
        "authors": [{"name": "Иван Иванов"}],
        "count": 5
    }
    response = apiclient.post("/api/books/delivery/", new_book_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.filter(title=new_book_data["title"]).exists()

@pytest.mark.django_db
def test_search_books_by_title(apiclient, create_books):
    response = apiclient.get("/api/books/?title=Книга 1")
    assert response.status_code == status.HTTP_200_OK
    assert any(book["title"].startswith("Книга 1") for book in response.data['results'])


@pytest.mark.django_db
def test_update_book_by_id(apiclient, create_books):
    book = Book.objects.first()
    updated_data = {"title": "Обновленное название"}
    response = apiclient.patch(f"/api/books/{book.id}/", updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    book.refresh_from_db()
    assert book.title == updated_data["title"]


@pytest.mark.django_db
def test_delete_book_by_id(apiclient, create_books):
    book = Book.objects.first()
    response = apiclient.delete(f"/api/books/{book.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_create_author(apiclient):
    new_author_data = {
        "name": "Новая книга"
    }
    response = apiclient.post("/api/authors/", new_author_data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Author.objects.filter(name=new_author_data["name"]).exists()

@pytest.mark.django_db
def test_update_author_by_id(apiclient, create_authors):
    author = Author.objects.first()
    updated_data = {"name": "Обновленное имя"}
    response = apiclient.patch(f"/api/authors/{author.id}/", updated_data, format="json")
    assert response.status_code == status.HTTP_200_OK
    author.refresh_from_db()
    assert author.name == updated_data["name"]


@pytest.mark.django_db
def test_delete_author_by_id(apiclient, create_authors):
    author = Author.objects.first()
    response = apiclient.delete(f"/api/authors/{author.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Author.objects.filter(id=author.id).exists()
