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
        python main.py -r ../test/myvcsrepo -w ../output -d -a
        python main.py -r ../test/myvcsrepo -w ../output -d -a -v -c
        python main.py -r ../test/myvcsrepo -w ../output -d -p -i in_author.csv -a

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
    parser.add_option("-d", "--dev",
                      action="store_true",
                      dest="dev",
                      default=False,
                      help="Retrieve developer name and save in CSV")
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
    xp_analyser = xpanalyser.XPAnalyser(options.repo, options.workdir)
    xp_analyser.retrieve_author_information_from_repo()
    if options.dev:
        xp_analyser.save_author_information_in_csv()
    if options.parse:
        xp_analyser.get_author_information_from_csv(options.in_csv)
    if options.analyse:
        xp_analyser.compute_experience()


if __name__ == "__main__":
    main()
