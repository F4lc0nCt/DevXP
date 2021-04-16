"""
Module for class XPAnalyser
"""

import csv
import datetime
import logging
import os

import authorcsv
import experience
import vcsmanager


class XPAnalyser:
    """
    Class which encapsulates an analysis of a VCS repository
    """

    OUTPUT_FILENAME = "experience.csv"
    DEFAULT_INCREMENT = 1

    def __init__(self, path, work_dir=""):
        """
        Class in charge of the analysis

        :param path: Path to the VCS repository to analyse
        :type path: str
        :param work_dir: Path to the working directory (for output and output file)
        :type work_dir: str
        """
        self.path = path
        self.vcs_mgr = vcsmanager.VCSManager(path)
        self.work_dir = work_dir
        self.csv_path = os.path.join(self.work_dir, XPAnalyser.OUTPUT_FILENAME)
        self.author_csv = None
        self.experiences = []

    def retrieve_author_information_from_repo(self):
        """
        Retrieve all the information of the author of the repository

        """
        logging.info('Retrieving author information from repository %s', self.path)
        self.vcs_mgr.build_author_dict()
        self.author_csv = authorcsv.AuthorCSV(self.vcs_mgr.author_dict, self.work_dir)

    def save_author_information_in_csv(self):
        """
        Write authors' information in a CSV file

        """
        self.author_csv.save_data_in_csv()

    def get_author_information_from_csv(self, path):
        """
        Retrieve authors' information from a CSV file

        :param path: Path to the CSV file
        :type path: str
        """
        self.author_csv.update_data_from_csv(os.path.join(self.work_dir, path))

    def compute_experience(self):
        """
        Compute from the start date of project (i.e. first commit) until today
        all the experience of the developer based on their first commit date and
        when they left the project (if they left it).

        """
        curr_date = self.vcs_mgr.first_commit_repo + datetime.timedelta(1)
        end_date = datetime.date.today()
        while curr_date <= end_date:
            curr_xp = experience.Experience(curr_date)
            for dev in self.vcs_mgr.author_dict.values():
                curr_xp.process_dev(dev)
            self.experiences.append(curr_xp)
            curr_date = XPAnalyser.increment_date(curr_date, XPAnalyser.DEFAULT_INCREMENT)
        self.save_analyse()

    @staticmethod
    def increment_date(date, nb_month):
        """
        Pratical method to increment a date of a number of month

        :param date: Start date to increment
        :type date: datetime.datetime.date
        :param nb_month: Number of months to add
        :type nb_month: int
        :return: Incremented date
        :rtype: datetime.date
        """
        next_month = ((date.month + nb_month) % datetime.date.max.month)
        next_year = date.year + ((date.month + nb_month) // datetime.date.max.month)
        if next_month == 0:
            next_month = 12
            next_year -= 1
        return datetime.date(next_year, next_month, 1)

    def save_analyse(self):
        """
        Save the analysis in a CSV file in the working directory

        """
        with open(self.csv_path, mode='w', newline='') as csv_file:
            xp_writer = csv.DictWriter(csv_file,
                                       fieldnames=experience.Experience.FIELDS.keys(),
                                       delimiter=';',
                                       quotechar='"',
                                       quoting=csv.QUOTE_MINIMAL)
            xp_writer.writeheader()
            try:
                [xp_writer.writerow(x.get_dict_values()) for x in self.experiences]
            except UnicodeEncodeError as exc:
                logging.error('Catch exception: %s', exc.reason)
