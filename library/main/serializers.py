from rest_framework import serializers
from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class InputAuthorSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if not all(char.isalpha() or char == '.' or char == ' ' for char in value):
            raise serializers.ValidationError("Поле name должно состоять только из букв, точек и пробелов.")
        return value

    class Meta:
        model = Author
        fields = ['name']
    



class BookSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if not all(char.isalnum() or char == ' ' for char in value):
            raise serializers.ValidationError("Поле title должно состоять только из букв, цифр и пробелов.")
        return value

    authors = InputAuthorSerializer(many=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'count']



    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        title = validated_data['title']
        count = validated_data['count']


        # Получаем список авторов
        names = [author_data.get('name') for author_data in authors_data]

        # Проверяем, существует ли книга с таким названием и авторами
        try:

            #book = Book.objects.get(title=title, authors__name__in=names)
            for i in names:
                book = Book.objects.get(title=title, authors__name=i)

            # Если книга найдена, увеличиваем счетчик
            book.count += count
            book.save()
        except Book.DoesNotExist:
            # Если книги нет, создаем новую
            book = Book.objects.create(**validated_data)


        for author_data in authors_data:
            name = author_data.get('name')
            author, created = Author.objects.get_or_create(name=name)
            if created:
                print(f"Новый автор '{name}' создан.")
            else:
                print(f"Автор '{name}' уже существует.")
            book.authors.add(author)
        
        return book



class BookSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        if not all(char.isalnum() or char == ' ' for char in value):
            raise serializers.ValidationError("Поле title должно состоять только из букв, цифр и пробелов.")
        return value

    authors = InputAuthorSerializer(many=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'count']



    def create(self, validated_data):
        print(validated_data)

