"""
Module for class VCSManager
"""

import datetime
import logging
import os
import subprocess
import sys

import developer


class VCSManager:
    """
    Class which realises operations on the VCS repository
    """

    GIT_LOG_CMD = 'git --git-dir={0}' + os.path.sep + '.git  --work-tree={0} log {1}'
    AUTHOR_FORMAT = '"--pretty=%an;%ae"'
    AUTHOR_DATE = '--author="{0}" --pretty="%aI"'

    def __init__(self, vcs_path):
        """
        Class in a charge of retrieving developer information from a VCS (Version Control System)

        :param vcs_path: Path to the VCS repository
        :type vcs_path: str
        """
        self.vcs_path = vcs_path
        self.max_number_of_authors = sys.maxsize
        self.author_dict = dict()
        self.first_commit_repo = datetime.date.max

    def build_author_dict(self):
        """
        Build the author directory by getting the authors list and their first/last commit dates

        """
        self.retrieve_author()
        self.retrieve_commit_date()

    def retrieve_author(self):
        """
        Get the authors list by using a command of the VCS

        """
        logging.info('Retrieving author')
        vcs_cmd = VCSManager.GIT_LOG_CMD.format(self.vcs_path, VCSManager.AUTHOR_FORMAT)
        logging.info(vcs_cmd)
        output = subprocess.check_output(vcs_cmd, shell=True).decode("utf-8")
        idx = 0
        log_percent = 0
        output_set = set(str(output).split('\n'))
        for line in output_set:
            if idx/len(output_set) > log_percent:
                logging.info('Processing Author: %.2f%%', 100*idx/len(output_set))
                log_percent += 0.1
            if idx > self.max_number_of_authors:
                logging.warning('Maximal number or author reached')
                break
            logging.debug('Processing line %s', line)
            idx += 1
            data = line.split(';')
            if len(data) != 2:
                continue
            dev = developer.Developer(data[0], data[1])
            self.author_dict[dev.uuid] = dev
        logging.info('Dictionary of author build - Nb Authors: %d', len(self.author_dict))

    def retrieve_commit_date(self):
        """
        Get the first and last commit dates of the author by using a command of the VCS

        """
        logging.info('Retrieving commit date')
        vcs_cmd = VCSManager.GIT_LOG_CMD.format(self.vcs_path, VCSManager.AUTHOR_DATE)
        logging.info(vcs_cmd)
        idx = 0
        log_percent = 0
        for dev in self.author_dict.values():
            if (idx/len(self.author_dict.values())) > log_percent:
                logging.info('Retrieving commit date: %f%%', 100*idx/len(self.author_dict.values()))
                log_percent += 0.1
            idx += 1
            logging.debug(vcs_cmd.format(dev.name))
            commit_dates = subprocess.check_output(vcs_cmd.format(dev.name),
                                                   shell=True).decode("utf-8")
            if commit_dates == '':
                continue
            dates_list = commit_dates.split('\n')
            first_date = dates_list[-2] if dates_list[-1] == '' else dates_list[-1]
            last_date = dates_list[0]
            logging.debug('Commit of %s - First: %s - Last: %s', dev.name, first_date, last_date)
            dev.set_first_commit_date(first_date)
            dev.set_last_commit_date(last_date)
            self.update_first_commit_date(dev.first_commit_date)

    def update_first_commit_date(self, date):
        """
        Compute the start date of the project based on the first commit dates
        of all the developers.

        :param date: New possible start date
        :type date: datetime.date
        """
        if date < self.first_commit_repo:
            logging.debug('First commit of repository is now: %s', date)
            self.first_commit_repo = date
