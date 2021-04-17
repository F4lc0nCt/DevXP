
import os
import csv
import developer


class AuthorCSV:

    OUTPUT_FILENAME = "author_data.csv"

    def __init__(self, dev_dict, work_dir):
        self.dev_dict = dev_dict
        self.work_dir = work_dir
        self.csv_path = os.path.join(self.work_dir, AuthorCSV.OUTPUT_FILENAME)

    def save_data_in_csv(self):
        with open(self.csv_path, mode='w', newline='') as csv_file:
            author_writer = csv.DictWriter(csv_file,
                                           fieldnames=developer.Developer.FIELDS.keys(),
                                           delimiter=';',
                                           quotechar='"',
                                           quoting=csv.QUOTE_MINIMAL)
            author_writer.writeheader()
            try:
                [author_writer.writerow(x.get_dict_values()) for x in self.dev_dict.values()]
            except UnicodeEncodeError as exc:
                print('Catch exception: {0}'.format(exc.reason))

    def update_data_from_csv(self):
        with open(self.csv_path, mode='r', newline='') as csv_file:
            author_reader = csv.DictReader(csv_file, delimiter=';',
                                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # TODO
            print(author_reader)
