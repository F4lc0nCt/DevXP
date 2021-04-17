
import datetime


class Experience:

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
        self.curr_date = curr_date
        self.nb_junior = 0
        self.nb_advanced = 0
        self.nb_senior = 0
        self.real_xp = datetime.timedelta(0)
        self.cumulative_xp = datetime.timedelta(0)

    def add_xp(self, real_xp, all_xp):
        if real_xp > datetime.timedelta(0):
            self.add_xp_category(Experience.get_xp_category(real_xp))
        self.real_xp += real_xp
        self.cumulative_xp += all_xp

    @staticmethod
    def get_xp_category(xp_value):
        if xp_value < Experience.ADVANCED_XP:
            return Experience.JUNIOR
        if xp_value < Experience.SENIOR_XP:
            return Experience.ADVANCED
        return Experience.SENIOR

    def add_xp_category(self, category):
        if category == Experience.JUNIOR:
            self.nb_junior += 1
        elif category == Experience.ADVANCED:
            self.nb_advanced += 1
        elif category == Experience.SENIOR:
            self.nb_senior += 1
        else:
            raise Exception('Unknown category {0}'.format(category))

    def process_dev(self, developer):
        real, cumulative = developer.get_experience(self.curr_date)
        self.add_xp(real, cumulative)

    def get_curr_date(self):
        return datetime.datetime.strftime(self.curr_date, "%Y-%m-%d")

    def get_values(self):
        return [self.get_curr_date(), self.real_xp.days, self.cumulative_xp.days, self.nb_junior,
                self.nb_advanced, self.nb_senior]

    def get_dict_values(self):
        res = {}
        for key, value in Experience.FIELDS.items():
            if datetime.timedelta.__instancecheck__(self.__getattribute__(value)):
                res[key] = self.__getattribute__(value).days
            else:
                res[key] = self.__getattribute__(value)
        return res
