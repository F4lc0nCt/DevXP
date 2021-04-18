"""
Module for class Developer
"""

import datetime
import hashlib
import logging


class Developer:
    """
    Class representing a developer
    """

    # Do not use term ID since it is not supported by Excel as the first Element
    FIELDS = {'UUID': 'uuid', 'Name': 'name', 'Email': 'email',
              'First Commit': 'first_commit_date', 'Last Commit': 'last_commit_date',
              'Has Left': 'has_left', 'Exclude': 'exclude', 'Aliases': 'aliases'}

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, name, email):
        """
        Create a structure to represent a developer

        :param name: Name of the developer
        :type name: str
        :param email: Email of the developer
        :type email: str
        """
        logging.debug('Creating Developer %s: %s', name, email)
        self.name = name
        self.email = email
        self.uuid = hashlib.md5(self.name.encode('utf8')).hexdigest()
        self.first_commit_date = None
        self.last_commit_date = None
        self.aliases = []
        self.has_left = False
        self.exclude = False

    def get_values(self):
        """
        Return a subset of the attributes as a list

        :return: List of a subset of the attributes
        :rtype: list
        """
        return [self.name, self.email, self.get_first_commit_date(),
                self.get_last_commit_date(), self.has_left, self.exclude, self.aliases]

    def get_dict_values(self):
        """
        Return a subset of the attributes as a dict

        :return: Dict of a subset of the attributes
        :rtype: dict
        """
        res = {}
        for key, value in Developer.FIELDS.items():
            res[key] = self.__getattribute__(value)
        return res

    def get_first_commit_date(self):
        """
        Get the first commit date as a string with the format %Y-%m-%d

        :return: First commit date
        :rtype: str
        """
        if self.first_commit_date is None:
            return ""
        return datetime.date.strftime(self.first_commit_date, Developer.DATE_FORMAT)

    def get_last_commit_date(self):
        """
        Get the last commit date as a string with the format %Y-%m-%d

        :return: Last commit date
        :rtype: str
        """
        if self.last_commit_date is None:
            return ""
        return datetime.date.strftime(self.last_commit_date, Developer.DATE_FORMAT)

    def set_first_commit_date(self, iso_date):
        """
        Set the first commit date of the developer

        :param iso_date: First commit date with the ISO 8601 format
        :type iso_date: str
        """
        self.first_commit_date = datetime.datetime.\
            strptime(iso_date.split('T')[0], Developer.DATE_FORMAT).date()

    def set_last_commit_date(self, iso_date):
        """
        Set the last commit date of the developer

        :param iso_date: Last commit date with the ISO 8601 format
        :type iso_date: str
        """
        self.last_commit_date = datetime.datetime.\
            strptime(iso_date.split('T')[0], Developer.DATE_FORMAT).date()

    def is_present(self, curr_date):
        """
        Tell if a developer was present in the project a specific date

        :param curr_date: Date on which presence of the developer has to be checked
        :type curr_date: str
        :return: Boolean telling if the developer was present at this date
        :rtype: bool
        """
        if curr_date < self.first_commit_date:
            return False
        if not self.has_left:
            return True
        return curr_date <= self.last_commit_date

    def get_experience(self, curr_date):
        """
        Give the experience of the developer at a specific date of the project

        :param curr_date: Date on which the computation of the experience has to
                          be done
        :type curr_date: str
        :return: Real XP and Cumulative XP
                 Real XP is the XP if the developer is still in the project
                 Cumulative XP is the XP of the developer during its all timeframe of
                 presence in the project
        :rtype: datetime.timedelta, datetime.timedelta
        """
        real_xp = datetime.timedelta(0)
        cumulative_xp = datetime.timedelta(0)
        if curr_date >= self.first_commit_date:
            if not self.has_left or (self.has_left and curr_date <= self.last_commit_date):
                real_xp = curr_date - self.first_commit_date
                cumulative_xp = real_xp
            else:
                cumulative_xp = self.last_commit_date - self.first_commit_date
        logging.debug('%s %s at %s - Real XP: %d days - Cumulative XP: %d days', self.uuid,
                      self.name, curr_date, real_xp.days, cumulative_xp.days)
        return real_xp, cumulative_xp

    def update_based_on_aliases(self):
        """
        Update the information of developer based on the updated field
        'has_left' and 'aliases'
        """
        logging.debug('Updating commit date of %s %s', self.uuid, self.name)
        for alias in self.aliases:
            if alias.has_left != self.has_left:
                raise ValueError('Incoherent presence state for {0} a.k.a. {1}'
                                 .format(self.name, alias.name))
            if alias.exclude:
                logging.info('Alias %s is excluded, so %s is also excluded', alias.name, self.name)
                self.exclude = True
            if alias.first_commit_date < self.first_commit_date:
                self.first_commit_date = alias.first_commit_date
            if alias.last_commit_date > self.last_commit_date:
                self.last_commit_date = alias.last_commit_date
