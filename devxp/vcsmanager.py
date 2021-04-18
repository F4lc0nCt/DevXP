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
    AUTHOR_DATE = '--author={0} --pretty="%aI"'

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

    def build_author_dict(self, full=True):
        """
        Build the author directory by getting the authors list and their first/last commit dates

        :param full: Retrieve also the date
        :type bool
        """
        self.retrieve_author()
        if full:
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
        dev_to_del = []
        for key, dev in self.author_dict.items():
            if (idx/len(self.author_dict.items())) > log_percent:
                logging.info('Retrieving commit date: %f%%', 100*idx/len(self.author_dict.items()))
                log_percent += 0.1
            idx += 1
            # repr() must be use to convert possible escape characters
            logging.debug(vcs_cmd.format(VCSManager.repr_spe(dev.name)))
            commit_dates = subprocess.check_output(vcs_cmd.format(
                VCSManager.repr_spe(dev.name)), shell=True).decode("utf-8")
            if commit_dates == '':
                logging.warning(vcs_cmd.format(VCSManager.repr_spe(dev.name)))
                logging.warning('%s does not have commit for %s', dev.name, commit_dates)
                dev_to_del.append(key)
                continue
            dates_list = commit_dates.split('\n')
            first_date = dates_list[-2] if dates_list[-1] == '' else dates_list[-1]
            last_date = dates_list[0]
            logging.debug('Commit of %s - First: %s - Last: %s', dev.name, first_date, last_date)
            if first_date is None or last_date is None:
                logging.warning('%s does not have commit for %s', dev.name, commit_dates)
                dev_to_del.append(key)
                continue
            dev.set_first_commit_date(first_date)
            dev.set_last_commit_date(last_date)
            self.update_first_commit_date(dev.first_commit_date)
        for key in dev_to_del:
            logging.warning('Deletion of %s %s', key, self.author_dict[key].name)
            del self.author_dict[key]

    def compute_first_commit_date(self):
        """
        Compute the start date of the project based on the first commit dates
        of all the developers.
        """
        for dev in self.author_dict.values():
            self.update_first_commit_date(dev.first_commit_date)

    def update_first_commit_date(self, date):
        """
        Update the start date of the project based on the first commit dates
        of all the developers.

        :param date: New possible start date
        :type date: datetime.date
        """
        if date < self.first_commit_repo:
            logging.debug('First commit of repository is now: %s', date)
            self.first_commit_repo = date

    @staticmethod
    def repr_spe(esc_str):
        """
        Own repr implementation to bypass double quote problem

        :param esc_str: String to change
        :type esc_str: str
        :return: New string that can be inserted in a commande line
        :rtype: str
        """
        esc_str = esc_str.replace('@', '@@')
        esc_str = esc_str.replace('"', '+ at +')
        esc_str = esc_str.replace("'", '- at -')
        esc_str = repr(esc_str)[1:-1]
        # Reverse the changes
        esc_str = esc_str.replace('- at -', "'")
        esc_str = esc_str.replace('+ at +', r'\"')
        esc_str = esc_str.replace('@@', '@')
        return '"%s"' % esc_str
