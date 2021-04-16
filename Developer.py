import os
import subprocess
import datetime
import csv

class Developer:

        def __init__(self, name, email):
            self.idx = 0
            self.name = name
            self.email = email
            self.id = hash(name)
            self.first_commit_date = None
            self.last_commit_date = None
            self.aliases = []
            self.has_gone = False

        def get_values(self):
            print(self.name)
            return [self.name, self.email, self.get_first_commit_date(), self.get_last_commit_date(), self.has_gone, self.aliases]

        def get_first_commit_date(self):
            return datetime.date.strftime(self.first_commit_date, "%Y-%m-%d")

        def get_last_commit_date(self):
            return datetime.date.strftime(self.last_commit_date, "%Y-%m-%d")

        def set_first_commit_date(self, iso_date):
            self.first_commit_date = datetime.datetime.strptime(iso_date.split('T')[0], "%Y-%m-%d").date()

        def set_last_commit_date(self, iso_date):
            self.last_commit_date = datetime.datetime.strptime(iso_date.split('T')[0], "%Y-%m-%d").date()

        def is_present(self, curr_date):
            if curr_date < self.first_commit_date:
                return False
            elif not self.has_gone:
                return True
            else:
                return curr_date <= self.last_commit_date

        def get_experience(self, curr_date, cumulative=False):
            real_xp = datetime.timedelta(0)
            cumulative_xp = datetime.timedelta(0)
            if curr_date < self.first_commit_date:
                pass
            elif not self.has_gone:
                real_xp = curr_date - self.first_commit_date
                cumulative_xp = real_xp
            else:
                if curr_date <= self.last_commit_date:
                    real_xp = curr_date - self.first_commit_date
                    cumulative_xp = curr_date - self.first_commit_date
                else:
                    cumulative_xp = self.last_commit_date - self.first_commit_date
            return real_xp, cumulative_xp


class Experience:

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
        self.real_experience = datetime.timedelta(0)
        self.cumulative_experience = datetime.timedelta(0)

    def add_xp(self, real_xp, all_xp):
        if real_xp > datetime.timedelta(0):
            self.add_xp_category(Experience.get_xp_category(real_xp))
        self.real_experience += real_xp
        self.cumulative_experience += all_xp

    @staticmethod
    def get_xp_category(xp):
        if xp <= Experience.JUNIOR_XP:
            return Experience.JUNIOR
        elif xp <= Experience.ADVANCED_XP:
            return Experience.ADVANCED
        else:
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
        return [self.get_curr_date(), self.real_experience.days, self.cumulative_experience.days, self.nb_junior, self.nb_advanced, self.nb_senior]



#git log --pretty="%an" | sort
#git log --author="$a" --pretty="Author: %an Last commit: %ai" | head -n1

if __name__ == "__main__":
    git_path = ".\\test\\gitignore"
    git_cmd_base = 'git --git-dir={0}\\.git  --work-tree={0} log --pretty="%an;%ae"'
    git_cmd = git_cmd_base.format(git_path)
    output = subprocess.check_output(git_cmd, shell=True).decode("utf-8")
    developer_dict = dict()
    LIMIT = 10
    IDX = 0
    for line in set(str(output).split('\n')):
        if IDX > LIMIT:
            break
        IDX += 1
        spl = line.split(';')
        if len(spl) != 2:
            continue
        dev = Developer(spl[0], spl[1])
        developer_dict[dev.id] = dev
    print(len(developer_dict))
    # Get first commit
    git_cmd_last_commit_base = 'git --git-dir={0}\\.git  --work-tree={0} log --author="{1}" --pretty="%aI"'
    for dev in developer_dict.values():
        commit_dates = subprocess.check_output(git_cmd_last_commit_base.format(git_path, dev.name), shell=True).decode("utf-8")
        print(commit_dates)
        if commit_dates == '':
            continue
        dates_list = commit_dates.split('\n')
        first_date = dates_list[0]
        last_date = dates_list[-2] if dates_list[-1] == '' else dates_list[-1]
        dev.set_first_commit_date(first_date)
        dev.set_last_commit_date(last_date)
        print(dev.get_values())
    print(developer_dict)

    with open('author_data.csv', mode='w', newline='') as csv_file:
        author_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        author_writer.writerow(['Name', 'Email', 'First Commit', 'Last Commit', 'Has Gone', 'Aliases'])
        [author_writer.writerow(x.get_values()) for x in developer_dict.values()]

    """
    update_developer_dict = {}
    with open('author_data.csv', mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        idx = 0
        for line in csv_reader:
            if line == 0:
                continue
            Developer"""

    start_date = datetime.date(2010, 1, 1)
    end_date = datetime.date.today()
    increment = datetime.timedelta
    experiences = []
    curr_date_val = start_date
    while curr_date_val <= end_date:
        curr_xp = Experience(curr_date_val)
        for dev in developer_dict.values():
            curr_xp.process_dev(dev)
        experiences.append(curr_xp)
        next_month = curr_date_val.month + 1 if curr_date_val.month < 12 else 1
        next_year = curr_date_val.year if next_month > 1 else curr_date_val.year +1
        curr_date_val = datetime.date(next_year, next_month, 1)

    with open('experience.csv', mode='w', newline='') as csv_file:
        xp_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        xp_writer.writerow(['Date', 'Current XP', 'Cumulative XP', 'NB JUNIOR', 'NB ADVANCED', 'NB SENIOR'])
        [xp_writer.writerow(x.get_values()) for x in experiences]


