from rest_framework import serializers
from .models import Book, Author
import logging 

logger = logging.getLogger(__name__) 

class AuthorSerializerList(serializers.ModelSerializer):
    books_count = serializers.IntegerField()
    class Meta:
        model = Author
        fields = ['id', 'name', 'books_count']

class AuthorSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if not all(char.isalpha() or char == '.' or char == ' ' for char in value):
            logger.warning("Поле name должно состоять только из букв, точек и пробелов.") 
            raise serializers.ValidationError("Поле name должно состоять только из букв, точек и пробелов.")
        return value
    class Meta:
        model = Author
        fields = ['id', 'name']


class InputAuthorSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if not all(char.isalpha() or char == '.' or char == ' ' for char in value):
            logger.warning("Поле name должно состоять только из букв, точек и пробелов.") 
            raise serializers.ValidationError("Поле name должно состоять только из букв, точек и пробелов.")
        return value

    class Meta:
        model = Author
        fields = ['name']
    

class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books_to_front = []
        for i in validated_data:
            authors_data = i.pop('authors')
            title = i['title']
            count = i['count']
            names = [author_data.get('name') for author_data in authors_data]
            try:
                for l in names:
                    book = Book.objects.get(title=title, authors__name=l)
                book.count += count
                book.save()
            except Book.DoesNotExist:
                book = Book.objects.create(**i)
            
            for author_data in authors_data:
                name = author_data.get('name')
                author, created = Author.objects.get_or_create(name=name)
                book.authors.add(author)
            
            books_to_front.append(book)
        
        return books_to_front



class BookSerializer(serializers.ModelSerializer):
    authors = InputAuthorSerializer(many=True)
    def validate_title(self, value):
        if not all(char.isalnum() or char == ' ' for char in value):
            raise serializers.ValidationError("Поле title должно состоять только из букв, цифр и пробелов.")
        return value

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        return value

    def validate_authors(self, value):
        if not value:
            raise serializers.ValidationError("Необходимо указать хотя бы одного автора.")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'count']
        # если на вход подается массив объектов, то обработка переходит в BookListSerializer
        list_serializer_class = BookListSerializer      

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        title = validated_data['title']
        count = validated_data['count']

        names = [author_data.get('name') for author_data in authors_data]
        # Проверяем, существует ли книга с таким названием и авторами, если такая книга есть, то увеличиваем счетчик
        # если такой нет, то создаем новую
        try:
            for i in names:
                book = Book.objects.get(title=title, authors__name=i)
            book.count += count
            book.save()
        except Book.DoesNotExist:
            book = Book.objects.create(**validated_data)
        # проверяем авторов, если автор не найден, то создаем нового
        for author_data in authors_data:
            name = author_data.get('name')
            author, created = Author.objects.get_or_create(name=name)
            if created:
                logger.info(f"Новый автор '{name}' создан.")
            else:
                logger.warning(f"Автор '{name}' уже существует.")
            book.authors.add(author)
        
        return book



