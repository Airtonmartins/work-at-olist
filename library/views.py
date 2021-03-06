from rest_framework import generics, status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorList(generics.ListAPIView):
    """
    Retrieve list of Authors from base.
    """
    serializer_class = AuthorSerializer

    @swagger_auto_schema(operation_description="Retrieve list of Authors",
        manual_parameters=[
            openapi.Parameter(name='name', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER)], 
        responses={200: AuthorSerializer(many=True)})
    def get_queryset(self):
        authors = Author.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            authors = authors.filter(name=name)
        return authors


class BookList(APIView):
    """
    Create a new Book.
    """

    @swagger_auto_schema(operation_description="Retrieve list of Books", 
        responses={200: BookSerializer(many=True)})
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create a new Book", 
        request_body=BookSerializer(),
        responses={200: BookSerializer()})
    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    """
    Retrieve, Update and Delete a Book instance.
    """

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(operation_description="Retrieve a Book instance", 
        responses={200: BookSerializer()})
    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Update a Book instance", 
        request_body=BookSerializer(),
        responses={200: BookSerializer()})
    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a Book instance")
    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
