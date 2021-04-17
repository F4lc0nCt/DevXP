
import datetime


class Developer:

    FIELDS = {'Name': 'name', 'Email': 'email',
              'First Commit': 'first_commit_date', 'Last Commit': 'last_commit_date',
              'Has Left': 'has_left', 'Aliases': 'aliases'}

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.hash_id = hash(name)
        self.first_commit_date = None
        self.last_commit_date = None
        self.aliases = []
        self.has_left = False

    def get_values(self):
        return [self.name, self.email, self.get_first_commit_date(),
                self.get_last_commit_date(), self.has_left, self.aliases]

    def get_dict_values(self):
        res = {}
        for key, value in Developer.FIELDS.items():
            if str.__instancecheck__(self.__getattribute__(value)):
                res[key] = self.__getattribute__(value)\
                    .encode('ascii', errors='ignore').decode('ascii')
            else:
                res[key] = self.__getattribute__(value)
        return res

    def get_first_commit_date(self):
        return datetime.date.strftime(self.first_commit_date, "%Y-%m-%d")

    def get_last_commit_date(self):
        return datetime.date.strftime(self.last_commit_date, "%Y-%m-%d")

    def set_first_commit_date(self, iso_date):
        self.first_commit_date = datetime.datetime.\
            strptime(iso_date.split('T')[0], "%Y-%m-%d").date()

    def set_last_commit_date(self, iso_date):
        self.last_commit_date = datetime.datetime.\
            strptime(iso_date.split('T')[0], "%Y-%m-%d").date()

    def is_present(self, curr_date):
        if curr_date < self.first_commit_date:
            return False
        if not self.has_left:
            return True
        return curr_date <= self.last_commit_date

    def get_experience(self, curr_date):
        real_xp = datetime.timedelta(0)
        cumulative_xp = datetime.timedelta(0)
        if curr_date < self.first_commit_date:
            pass
        elif not self.has_left:
            real_xp = curr_date - self.first_commit_date
            cumulative_xp = real_xp
        else:
            if curr_date <= self.last_commit_date:
                real_xp = curr_date - self.first_commit_date
                cumulative_xp = curr_date - self.first_commit_date
            else:
                cumulative_xp = self.last_commit_date - self.first_commit_date
        return real_xp, cumulative_xp
