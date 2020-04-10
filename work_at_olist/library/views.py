from rest_framework import generics

from .models import Author
from .serializers import AuthorSerializer


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