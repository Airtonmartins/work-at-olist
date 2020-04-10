from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from library.models import Author

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
        
    

        
