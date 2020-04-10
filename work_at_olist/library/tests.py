import datetime
from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from rest_framework import status
from django.test import TestCase
from django.urls import reverse


from rest_framework.test import APITestCase
from library.models import Author, Book


class ImportAuthorsTest(TestCase):
    def test_command_output_success(self):
        """
        Checks if import_authors command is saving the authors
        """
        out = StringIO()
        call_command('import_authors', 'authors.csv', stdout=out)
        authors = Author.objects.all()
        self.assertIn('Reading:authors.csv', out.getvalue())
        self.assertIn('- Author Luciano Ramalho saved', out.getvalue())
        self.assertIn('- Author Osvaldo Santana Neto saved', out.getvalue())
        self.assertIn('- Author David Beazley saved', out.getvalue())
        self.assertIn('- Author Chetan Giridhar saved', out.getvalue())
        self.assertIn('- Author Brian K. Jones saved', out.getvalue())
        self.assertIn('- Author J.K Rowling saved', out.getvalue())
        self.assertIn('Authors saved successfully', out.getvalue())
        self.assertEqual(len(authors), 6)
    
    def test_command_output_fail(self):
        """
        Checks error in import_authors command when try saving the authors
        without a CSV file
        """
        out = StringIO()
        with self.assertRaises(CommandError):
            call_command('import_authors', 'books.csv', stdout=out)
        
    
class AuthorTests(APITestCase):

        def setUp(self):
            Author.objects.create(name="Neris")

        def test_list_authors(self):
            """
            Checks basic functioning of the GET /authors endpoint
            """

            url = reverse('authors-list')
            response = self.client.get(url)
            status_code = response.status_code
            response_body = response.data
            results = response_body['results']
            self.assertEqual(status_code, status.HTTP_200_OK)
            self.assertEqual(response_body['count'], 1)
            self.assertEqual(len(results), 1)

        def test_search_author(self):
            """
            Checks basic functioning of the GET /authors?name=author endpoint
            """

            Author.objects.create(name="Martins")
            url = reverse('authors-list') + '?name=Neris'
            response = self.client.get(url)
            status_code = response.status_code
            response_body = response.data
            results = response_body['results']
            authors = Author.objects.all()
            self.assertEqual(status_code, status.HTTP_200_OK)
            self.assertEqual(response_body['count'], 1)
            self.assertEqual(authors.count(), 2)
            self.assertEqual(len(results), 1)


class BookTests(APITestCase):

    def setUp(self):
        Author.objects.create(name="Neris")
        self.url_list = reverse('books-list')
        self.request_body = {
            "name": "Book",
            "edition": 1,
            "publication_year": "2019",
            "authors": [1]
        }
        self.url_detail = reverse('books-detail',  kwargs={'pk':1})
    
    def test_create_book(self):
        """
        Checks creating Book using the POST /book endpoint
        """
        response = self.client.post(self.url_list, 
            data=self.request_body, format='json')
        status_code = response.status_code
        book = Book.objects.first()
        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertEqual(book.name,"Book")
        self.assertEqual(book.edition, 1)
        self.assertEqual(book.publication_year, datetime.date(2019, 1, 1))
        self.assertEqual(book.authors.count(), 1)
    
    def test_list_books(self):
        """
        Checks basic functioning of the GET /books endpoint
        """
        self.client.post(self.url_list, data=self.request_body, format='json')
        response = self.client.get(self.url_list)
        status_code = response.status_code
        response_body = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body), 1)
    
    def test_get_book(self):
        """
        Checks basic functioning of the GET /books/id endpoint
        """
        self.client.post(self.url_list, data=self.request_body, format='json')
        response = self.client.get(self.url_detail)
        status_code = response.status_code
        response_body = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['name'], 'Book')
        self.assertEqual(response_body['edition'], 1)
        self.assertEqual(response_body['publication_year'], "2019")
        self.assertEqual(response_body['authors'], [1])

    def test_update_book(self):
        """
        Checks updating Book using the PUT /books/id endpoint
        """

        self.client.post(self.url_list, data=self.request_body, format='json')
        self.request_body['edition'] = 2
        self.request_body['publication_year'] = '2020'
        response = self.client.put(self.url_detail, 
            data=self.request_body, 
            format='json')
        status_code = response.status_code
        response_body = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_body['name'], 'Book')
        self.assertEqual(response_body['edition'], 2)
        self.assertEqual(response_body['publication_year'], "2020")
        self.assertEqual(response_body['authors'], [1])
