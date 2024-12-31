from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

# Create your views here.




class DeliveryBooks(CreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [JSONParser]
    
    def post(self, request):
        delivery_books = request.data


        return Response(delivery_books)






class GetAllCreateBooks(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # поиск по названию книги api/books/?title=название
    def get_queryset(self):
        queryset = Book.objects.all().order_by('id')
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
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


        