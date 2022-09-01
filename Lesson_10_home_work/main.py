"""This is a main file of Flask app ruling all processes"""
from classes import CandidateFinder

DATA_SOURCE = 'candidates.json'


def main(filename):
    """Main function creates an instance of CandidateFinder and starts Flask
    app.

    :param filename: A name of JSON file with candidates' data
    """
    finder = CandidateFinder(filename)
    finder.set_rules()
    finder.run_app()


if __name__ == '__main__':
    main(DATA_SOURCE)
