from django.shortcuts import render
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer, AuthorSerializerList
from rest_framework.response import Response
from rest_framework import status
from .paginator import CustomPagination
import logging 

logger = logging.getLogger(__name__) 


class GetAuthorStat(ListAPIView):
    queryset = Author.objects.annotate(books_count=Count('books')).order_by('-books_count')
    serializer_class = AuthorSerializerList
    pagination_class = CustomPagination 


class GetAuthorStatID(RetrieveAPIView):
    queryset = Author.objects.all().annotate(books_count=Count('books'))
    serializer_class = AuthorSerializerList
    lookup_field = 'id'


class GetTopCopies(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer  
    # получить топ книг api/books/copies?top=N - топ N книг по количеству экземпляров
    def get_queryset(self):
        queryset = Book.objects.all().order_by('-count')
        top_number = self.request.query_params.get('top')
        if top_number and top_number.isdigit() and int(top_number) > 0:
            queryset = queryset[:int(top_number)]
        else:
            logger.warning(f"{top_number} - некорректный формат данных")
        logger.info(f"Получены топ {top_number} книг по количеству копий.")
        return queryset


class DeliveryBooks(CreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Книги успешно созданы: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Ошибка при создании книг: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllCreateBooks(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # поиск по названию книги api/books/?title=название
    def get_queryset(self):
        queryset = Book.objects.all().order_by('id')
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        logger.info(f"Поиск книг по названию: {title}")
        return queryset

    
class GetDeleteUpdateBookById(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'


class GetAllCreateAuthors(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    

class GetDeleteUpdateAuthorById(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'


        