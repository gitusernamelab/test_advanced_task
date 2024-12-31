import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'library.settings'
django.setup()
from django.test.utils import setup_test_environment, teardown_test_environment
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer
from django.urls import reverse
import pytest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import warnings


setup_test_environment()


class TestBooks(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Создание авторов
        self.author_1 = Author.objects.create(name="Автор 1")
        self.author_2 = Author.objects.create(name="Автор 2")

        # Создание книг
        self.book_1 = Book.objects.create(title="Книга 1")
        self.book_2 = Book.objects.create(title="Книга 2")
        self.book_1.authors.add(self.author_1)
        self.book_2.authors.add(self.author_2)


    def test_get_all_books(self):
        url = reverse('get-all-create-books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    

    def test_create_book(self):
        data = {
            "title": "Новая книга",
            "authors": ["Автор 1"]
        }
        
        url = reverse('get-all-create-books')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Новая книга", response.data['title'])
    
    def test_update_book(self):
        data = {
                    "title": "Обновленная книга",
                    "authors": ["Автор 1"]
                }
        url = reverse('get-delete-update-books', kwargs={'id': self.book_1.id})
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Обновленная книга')
    
    def test_delete_book(self):
        url = reverse('get-delete-update-books', kwargs={'id': self.book_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book_1.id).exists())


class TestAuthors(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Создание авторов
        self.author_1 = Author.objects.create(name="Автор 1")
        self.author_2 = Author.objects.create(name="Автор 2")

    def test_get_all_authors(self):
        url = reverse('get-all-create-authors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_author(self):
        data = {"name": "Новый автор"}
        url = reverse('get-all-create-authors')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Новый автор", response.data['name'])

    def test_get_single_author(self):
        url = reverse('get-delete-update-authors', kwargs={'id': self.author_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Автор 1')

    def test_update_author(self):
        data = {"name": "Обновленный автор"}
        url = reverse('get-delete-update-authors', kwargs={'id': self.author_1.id})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Обновленный автор')

    def test_delete_author(self):
        url = reverse('get-delete-update-authors', kwargs={'id': self.author_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author_1.id).exists())


teardown_test_environment()