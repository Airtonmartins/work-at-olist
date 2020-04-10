from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorList(generics.ListAPIView):
    """
    Retrieve list of Authors from base.
    """
    serializer_class = AuthorSerializer

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

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)