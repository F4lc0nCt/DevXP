"""
Module for class Experience
"""

import datetime


class Experience:
    """
    Class allowing to process experience of a project at a specific date
    """

    FIELDS = {'Date': 'curr_date', 'Real XP': 'real_xp', 'Cumulative XP': 'cumulative_xp',
              'Nb Junior': 'nb_junior', 'Nb Advanced': 'nb_advanced',
              'Nb Senior': 'nb_senior'}

    JUNIOR_XP = datetime.timedelta(182)
    ADVANCED_XP = datetime.timedelta(365)
    SENIOR_XP = datetime.timedelta(730)

    JUNIOR = 1
    ADVANCED = 2
    SENIOR = 3

    def __init__(self, curr_date):
        """
        Represent the experience of a project a specific date

        :param curr_date: Date of the project to analyse
        :type curr_date: str
        """
        self.curr_date = curr_date
        self.nb_junior = 0
        self.nb_advanced = 0
        self.nb_senior = 0
        self.real_xp = datetime.timedelta(0)
        self.cumulative_xp = datetime.timedelta(0)

    def add_xp(self, real_xp, all_xp):
        """
        Add Real XP and Cumulative XP of a developer to the project.

        :param real_xp: Real XP of the developer
        :type real_xp: datetime.timedelta
        :param all_xp: Cumulative XP of the developer
        :type all_xp: datetime.timedelta
        """
        if real_xp > datetime.timedelta(0):
            self.add_xp_category(Experience.get_xp_category(real_xp))
        self.real_xp += real_xp
        self.cumulative_xp += all_xp

    @staticmethod
    def get_xp_category(xp_value):
        """
        Get the category of a developer based on his/her/its experience

        :param xp_value: Experience of the developer
        :type xp_value: datetime.timedelta
        :return: The category of experience of the developer
        :rtype: int
        """
        if xp_value < Experience.ADVANCED_XP:
            return Experience.JUNIOR
        if xp_value < Experience.SENIOR_XP:
            return Experience.ADVANCED
        return Experience.SENIOR

    def add_xp_category(self, category):
        """
        Add a profile to the current experience count

        :param category: Profile of experience
        :type category: int
        """
        if category == Experience.JUNIOR:
            self.nb_junior += 1
        elif category == Experience.ADVANCED:
            self.nb_advanced += 1
        elif category == Experience.SENIOR:
            self.nb_senior += 1
        else:
            raise ValueError('Unknown category {0}'.format(category))

    def process_dev(self, developer):
        """
        Process the experience of a developer

        :param developer: Developer to process
        :type developer: Developer
        """
        real, cumulative = developer.get_experience(self.curr_date)
        self.add_xp(real, cumulative)

    def get_curr_date(self):
        """
        Get the current date of the analyse as a string with the format %Y-%m-%d

        :return: Date with the format %Y-%m-%d
        :rtype: str
        """
        return datetime.datetime.strftime(self.curr_date, "%Y-%m-%d")

    def get_values(self):
        """
        Return a subset of the attributes as a list

        :return: List of a subset of the attributes
        :rtype: list
        """
        return [self.get_curr_date(), self.real_xp.days, self.cumulative_xp.days, self.nb_junior,
                self.nb_advanced, self.nb_senior]

    def get_dict_values(self):
        """
        Return a subset of the attributes as a dict

        :return: Dict of a subset of the attributes
        :rtype: dict
        """
        res = {}
        for key, value in Experience.FIELDS.items():
            if datetime.timedelta.__instancecheck__(self.__getattribute__(value)):
                res[key] = self.__getattribute__(value).days
            else:
                res[key] = self.__getattribute__(value)
        return res
