#! python
"""
Module main method
For compatibility, with Python2, the module optparse is used.
"""

import logging
import optparse
import os

import xpanalyser


def main():
    """
    Main method to call the analyser

    Examples of commands :
        python main.py -r ../test/myvcsrepo -w ../output -d -o -a
        python main.py -r ../test/myvcsrepo -w ../output -d -a -v -c
        python main.py -r ../test/myvcsrepo -w ../output -p -i in_author.csv -a

    :return: Nothing
    :rtype: None
    """
    parser = optparse.OptionParser(usage="usage: %prog [options] filename",
                                   version="%prog 1.0")
    parser.add_option("-r", "--repo",
                      action="store",
                      dest="repo",
                      default=".",
                      help="Version control repository to analyse")
    parser.add_option("-d", "--date",
                      action="store_true",
                      dest="date",
                      default=False,
                      help="Retrieve commit date")
    parser.add_option("-o", "--out",
                      action="store_true",
                      dest="out",
                      default=False,
                      help="Save author data in CSV for post-processing")
    parser.add_option("-p", "--parse",
                      action="store_true",
                      dest="parse",
                      default=False,
                      help="Parse CSV file")
    parser.add_option("-i", "--in_csv",
                      action="store",
                      dest="in_csv",
                      default="in_author.csv",
                      help="CSV Filename to parse")
    parser.add_option("-a", "--analyse",
                      action="store_true",
                      dest="analyse",
                      default=False,
                      help="Launch analyse")
    parser.add_option("-w", "--workdir",
                      action="store",
                      dest="workdir",
                      default=".",
                      help="Working directory")
    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="Working directory")
    parser.add_option("-c", "--console",
                      action="store_true",
                      dest="console",
                      default=False,
                      help="Redirect trace to console")
    (options, args) = parser.parse_args()

    # Configure Logging
    log_level = logging.DEBUG if options.verbose else logging.INFO
    console_level = log_level if options.console else logging.ERROR

    logger = logging.getLogger()
    logger.setLevel(log_level)
    file_handler = logging.FileHandler(filename=os.path.join(options.workdir, 'devxp.log'),
                                       mode="w",
                                       encoding="UTF-8")
    file_handler.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info('\n\n\nNew run with options: %s and args: %s', options, args)
    # Check consistency
    if not options.date and not options.parse:
        raise RuntimeError('Users must use at least one option:'
                           'date retrieving (-d) or date parsing (-p).')
    xp_analyser = xpanalyser.XPAnalyser(options.repo, options.workdir)
    xp_analyser.retrieve_author_information_from_repo(options.date)
    if options.out:
        xp_analyser.save_author_information_in_csv()
    if options.parse:
        xp_analyser.get_author_information_from_csv(options.in_csv)
    if options.analyse:
        xp_analyser.compute_experience()


if __name__ == "__main__":
    main()
