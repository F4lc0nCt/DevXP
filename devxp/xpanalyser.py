
import os
import datetime
import csv
import gitmanager
import experience
import authorcsv


class XPAnalyser:

    OUTPUT_FILENAME = "experience.csv"
    DEFAULT_INCREMENT = 1

    def __init__(self, path, work_dir=""):
        self.git_mgr = gitmanager.GitManager(path)
        self.git_mgr.build_author_dict()
        self.work_dir = work_dir
        self.author_csv = authorcsv.AuthorCSV(self.git_mgr.author_dict, self.work_dir)
        self.author_csv.save_data_in_csv()
        self.csv_path = os.path.join(self.work_dir, XPAnalyser.OUTPUT_FILENAME)
        self.experiences = []

    def compute_experience(self):
        curr_date = self.git_mgr.first_commit_repo + datetime.timedelta(1)
        end_date = datetime.date.today()
        while curr_date <= end_date:
            curr_xp = experience.Experience(curr_date)
            for dev in self.git_mgr.author_dict.values():
                curr_xp.process_dev(dev)
            self.experiences.append(curr_xp)
            curr_date = XPAnalyser.increment_date(curr_date, XPAnalyser.DEFAULT_INCREMENT)
        self.save_analyse()

    @staticmethod
    def increment_date(date, nb_month):
        next_month = ((date.month + nb_month) % datetime.date.max.month)
        next_year = date.year + ((date.month + nb_month) // datetime.date.max.month)
        if next_month == 0:
            next_month = 12
            next_year -= 1
        return datetime.date(next_year, next_month, 1)

    def save_analyse(self):
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
                print('Catch exception: {0}'.format(exc.reason))