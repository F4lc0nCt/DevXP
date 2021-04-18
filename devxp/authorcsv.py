"""
Module for class AuthorCSV
"""

import csv
import logging
import os

import developer


class AuthorCSV:
    """
    Class in charge do conversion between a developer dictionary and a CSV file.
    """

    OUTPUT_FILENAME = "out_author.csv"

    def __init__(self, dev_dict, work_dir):
        """
        Allow to do conversion between a developer dictionary and a CSV file.

        :param dev_dict: Developer dictionary
        :type dev_dict: dict(str->Developer)
        :param work_dir: Directory where are located CSV
        :type work_dir: str
        """
        self.dev_dict = dev_dict
        self.work_dir = work_dir
        self.csv_path = os.path.join(self.work_dir, AuthorCSV.OUTPUT_FILENAME)

    def save_data_in_csv(self):
        """
        Save the developer dictionary of the class in the CSV.
        """
        logging.info('Saving author information in %s', self.csv_path)
        with open(self.csv_path, mode='w', newline='', encoding='UTF-8') as csv_file:
            author_writer = csv.DictWriter(csv_file,
                                           fieldnames=developer.Developer.FIELDS.keys(),
                                           delimiter=';',
                                           quotechar='"',
                                           quoting=csv.QUOTE_MINIMAL)
            author_writer.writeheader()
            try:
                [author_writer.writerow(x.get_dict_values()) for x in self.dev_dict.values()]
            except UnicodeEncodeError as exc:
                logging.error('Catch exception: %s', exc.reason)

    def update_data_from_csv(self, path):
        """
        Retrieve information from a modified CSV file to update the developer information
        such as 'has_left' and 'aliases'

        :param path: Input CSV path
        :type path: str
        """
        logging.info('Retrieving author information from %s', path)
        with open(path, mode='r', newline='', encoding='UTF-8') as csv_file:
            author_reader = csv.DictReader(csv_file, delimiter=';',
                                           quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in author_reader:
                # Check if hte uuid is present
                uuid = row['UUID']
                if uuid not in self.dev_dict.keys():
                    raise ValueError('Unknown developer {0}'.format(row))
                # Update the has_left attribute
                self.dev_dict[uuid].has_left = row['Has Left'].lower() == "true"
                # Update First Commit Date
                first_commit_from_csv = row['First Commit']
                if first_commit_from_csv != self.dev_dict[uuid].get_first_commit_date():
                    logging.info('Change first commit date of %s - old %s - new %s',
                                 self.dev_dict[uuid].name,
                                 self.dev_dict[uuid].get_first_commit_date(),
                                 first_commit_from_csv)
                    self.dev_dict[uuid].set_first_commit_date(first_commit_from_csv)
                # Update First Commit Date
                last_commit_from_csv = row['Last Commit']
                if last_commit_from_csv != self.dev_dict[uuid].get_last_commit_date():
                    logging.info('Change last commit date of %s - old %s - new %s',
                                 self.dev_dict[uuid].name,
                                 self.dev_dict[uuid].get_last_commit_date(),
                                 last_commit_from_csv)
                    self.dev_dict[uuid].set_last_commit_date(last_commit_from_csv)
                # Update Aliases
                if row['Aliases'] != '[]':
                    self.dev_dict[uuid].aliases = list(map(int, row['Aliases'].split('_')))
        logging.info('Update of Author dictionary')
        uuid_to_delete = []
        for key, dev in self.dev_dict.items():
            uuid_aliases = dev.aliases.copy()
            dev.aliases.clear()
            for alias in uuid_aliases:
                logging.info('Linking UUID %s to %s %s', alias, key, dev.name)
                dev.aliases.append(self.dev_dict[alias])
                uuid_to_delete.append(alias)
            dev.update_based_on_aliases()
        for alias in uuid_to_delete:
            logging.debug('Deleting UUID %s', alias)
            del self.dev_dict[alias]
