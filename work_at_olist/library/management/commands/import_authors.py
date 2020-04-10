import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from library.models import Author


class Command(BaseCommand):
    help = "Import the Authors from CSV into the database. " \
        "Insert the CSV name in the arguments"

    def add_arguments(self, parser):
        parser.add_argument('filename',
            nargs=1,
            type=str,
            help="Insert the CSV name in the arguments.")

    def get_csv_file(self, filename):
        app_path = apps.get_app_config('library').path
        file_path = os.path.join(app_path, "management",
                                 "commands", filename)
        return file_path
    
    def check_headers_incorrect(self, headers):
        return (headers == None or len(headers) != 1)

    def save_author(self, name):
        try:
            Author.objects.create(name=name)
        except Exception as e:
            raise CommandError("Error in inserting Author: {}".format(str(e)))
    
    def handle(self, *args, **kwargs):
        filename = kwargs['filename'][0]
        self.stdout.write(self.style.SUCCESS('Reading:{}'.format(filename)))
        file_path = self.get_csv_file(filename)
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                headers = next(csv_reader, None)
                if self.check_headers_incorrect(headers):
                    raise CommandError("File {} does not in the correct " \
                        "format".format(file_path))
                
                for row in csv_reader:
                    if row != "":
                        author_name = row[0].strip()
                        self.save_author(author_name)
                        self.stdout.write(
                            self.style.SUCCESS('- Author {} saved'.format(
                                author_name)))

                self.stdout.write(self.style.SUCCESS('Authors saved successfully'))

        except FileNotFoundError:
            raise CommandError("File {} does not exist".format(
                file_path)) 
