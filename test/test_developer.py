
import unittest
import hashlib
import datetime

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from devxp import developer


class TestDeveloper(unittest.TestCase):

    TEST_NAME = 'Joe'
    TEST_EMAIL = 'joe@happy.com'

    def test_constructor(self):
        test_hash = hashlib.md5(self.TEST_NAME.encode('utf8')).hexdigest()
        dev = developer.Developer(self.TEST_NAME, self.TEST_EMAIL)
        self.assertEqual(dev.name, self.TEST_NAME)
        self.assertEqual(dev.email, self.TEST_EMAIL)
        self.assertEqual(dev.uuid, test_hash)
        self.assertEqual(dev.first_commit_date, None)
        self.assertEqual(dev.last_commit_date, None)
        self.assertEqual(len(dev.aliases), 0)
        self.assertEqual(dev.has_left, False)
        self.assertEqual(dev.exclude, False)

    def test_getter_setter(self):
        test_hash = hashlib.md5(self.TEST_NAME.encode('utf8')).hexdigest()
        first_commit_date = datetime.date(2000, 1, 1)
        last_commit_date = datetime.date(2020, 6, 15)
        first_commit = datetime.datetime.strftime(first_commit_date, "%Y-%m-%d")
        last_commit = datetime.datetime.strftime(last_commit_date, "%Y-%m-%d")
        dev = developer.Developer(self.TEST_NAME, self.TEST_EMAIL)
        dev.set_first_commit_date(first_commit)
        dev.set_last_commit_date(last_commit)
        self.assertEqual(dev.get_first_commit_date(), first_commit)
        self.assertEqual(dev.get_last_commit_date(), last_commit)
        all_values = dev.get_values()
        self.assertEqual(len(all_values), 7)
        self.assertEqual(all_values[0], self.TEST_NAME)
        self.assertEqual(all_values[1], self.TEST_EMAIL)
        self.assertEqual(all_values[2], first_commit)
        self.assertEqual(all_values[3], last_commit)
        self.assertEqual(all_values[4], False)
        self.assertEqual(all_values[5], False)
        self.assertEqual(len(all_values[6]), 0)

        all_dict_values = dev.get_dict_values()
        self.assertTrue('UUID' in all_dict_values.keys())
        self.assertEqual(all_dict_values['UUID'], test_hash)
        self.assertTrue('Name' in all_dict_values.keys())
        self.assertEqual(all_dict_values['Name'], self.TEST_NAME)
        self.assertTrue('Email' in all_dict_values.keys())
        self.assertEqual(all_dict_values['Email'], self.TEST_EMAIL)
        self.assertTrue('First Commit' in all_dict_values.keys())
        self.assertEqual(all_dict_values['First Commit'], first_commit_date)
        self.assertTrue('Last Commit' in all_dict_values.keys())
        self.assertEqual(all_dict_values['Last Commit'], last_commit_date)
        self.assertTrue('Has Left' in all_dict_values.keys())
        self.assertEqual(all_dict_values['Has Left'], False)
        self.assertTrue('Exclude' in all_dict_values.keys())
        self.assertEqual(all_dict_values['Exclude'], False)
        self.assertTrue('Aliases' in all_dict_values.keys())
        self.assertEqual(len(all_dict_values['Aliases']), 0)

    def test_is_present(self):
        first_commit = '2000-01-01'
        last_commit = '2010-06-15'
        dev = developer.Developer(self.TEST_NAME, self.TEST_EMAIL)
        dev.set_first_commit_date(first_commit)
        dev.set_last_commit_date(last_commit)
        self.assertFalse(dev.is_present(datetime.date(1995, 3, 6)))
        self.assertTrue(dev.is_present(datetime.date(2003, 2, 15)))
        self.assertTrue(dev.is_present(datetime.date(2018, 9, 21)))
        dev.has_left = True
        self.assertFalse(dev.is_present(datetime.date(2018, 9, 21)))

    def test_get_experience(self):
        first_commit = '2012-03-01'
        last_commit = '2012-05-01'
        dev = developer.Developer(self.TEST_NAME, self.TEST_EMAIL)
        dev.has_left = True
        dev.set_first_commit_date(first_commit)
        dev.set_last_commit_date(last_commit)
        real_xp, cumulative_xp = dev.get_experience(datetime.date(2012, 2, 1))
        self.assertEqual(real_xp.days, 0)
        self.assertEqual(cumulative_xp.days, 0)
        real_xp, cumulative_xp = dev.get_experience(datetime.date(2012, 3, 15))
        self.assertEqual(real_xp.days, 14)
        self.assertEqual(cumulative_xp.days, 14)
        real_xp, cumulative_xp = dev.get_experience(datetime.date(2012, 6, 15))
        self.assertEqual(real_xp.days, 0)
        self.assertEqual(cumulative_xp.days, 61)

    def test_update_alias(self):
        first_commit = '2012-03-01'
        last_commit = '2012-05-01'
        first_commit_alias = '2010-02-01'
        last_commit_alias = '2015-06-19'
        dev = developer.Developer(self.TEST_NAME, self.TEST_EMAIL)
        dev_alias = developer.Developer('alias_'+self.TEST_NAME, self.TEST_EMAIL)
        dev.has_left = False
        dev.set_first_commit_date(first_commit)
        dev.set_last_commit_date(last_commit)
        dev_alias.set_first_commit_date(first_commit_alias)
        dev_alias.set_last_commit_date(last_commit_alias)
        dev.aliases.append(dev_alias)
        dev.update_based_on_aliases()
        self.assertEqual(dev.get_first_commit_date(), first_commit_alias)
        self.assertEqual(dev.get_last_commit_date(), last_commit_alias)
        dev_alias.exclude = True
        dev.update_based_on_aliases()
        self.assertTrue(dev.exclude)
        dev_alias.has_left = True
        exception_raised = False
        try:
            dev.update_based_on_aliases()
        except ValueError as e:
            self.assertEqual(str(e), 'Incoherent presence state for {0} a.k.a. alias_{0}'.format(self.TEST_NAME))
            exception_raised = True
        self.assertTrue(exception_raised, 'Exception not raised')


if __name__ == '__main__':
    unittest.main()
