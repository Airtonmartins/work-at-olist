
from rest_framework import serializers
from library.models import Book


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=40)


class BookSerializer(serializers.ModelSerializer):
    publication_year = serializers.DateField(format="%Y", input_formats=['%Y'])

    class Meta:
        model = Book
        fields = ['id', 'name', 'edition','publication_year', 'authors']