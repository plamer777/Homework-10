"""The module contains a class that is an interface for comfortable work with
Flask"""
import json
from flask import Flask


class CandidateFinder:
    """The CandidateFinder provides fields and methods to work with
    Flask.
    :param filename: A json file with candidates' data
    """

    def __init__(self, filename):

        self.app = Flask(__name__)
        # candidates' data loads during initialization
        self.candidates = self.load_candidates(filename)

    @staticmethod
    def load_candidates(filename: str) -> list:
        """The staticmethod loads candidates list.

        :param filename: json file

        :return:
            data_list - a list of dicts
            """
        try:
            with open(filename, encoding='utf-8') as fin:
                data_list = json.load(fin)

        except FileNotFoundError:
            print(f'Файл {filename} не найден')
            return []

        except json.JSONDecodeError:
            print(f'Не удалось обработать данные из файла')
            return []

        return data_list

    def get_all(self) -> str:
        """This method used like a view for Flask route.

        :return:
            html styled string with candidates' name, position and skills"""

        all_candidates = ''

        for candidate in self.candidates:

            # a supportive data list to create string with candidates' data
            candidate_data = []

            name = f"Имя кандидата: {candidate.get('name', None)}"
            position = f"Позиция: {candidate.get('position', None)}"
            skills = f"Навыки: {candidate.get('skills', None)}"

            # checking if data was received
            if name and position and skills:

                candidate_data.extend((name, position, skills))

                # creation a string with candidates' data'
                all_candidates += '\n'.join(candidate_data) + '\n\n'

        return f'<pre>{all_candidates}</pre>' \
            if all_candidates else 'Список кандидатов пуст'

    def get_by_pk(self, pk: int) -> str:
        """One more Flask view.
        :return:
            html styled string with a certain candidate's data
            finding by number or info that candidate isn't found
            """
        for candidate in self.candidates:

            # if candidate is found then prepare a string with data
            if candidate.get('pk', None) == pk:

                photo_url = candidate.get('picture', None)
                name = f"Имя кандидата: {candidate.get('name', None)}"
                position = f"Позиция: {candidate.get('position', None)}"
                skills = f"Навыки: {candidate.get('skills', None)}"

                candidate_data = '\n'.join((name, position, skills))

                return f"<img src={photo_url}>" \
                       f"<pre>" \
                       f"{candidate_data}" \
                       f"</pre>"

        else:
            return f"Нет такого кандидата"

    def get_by_skill(self, skill_name: str) -> str:
        """This is a Flask view func.

        :param skill_name: a desired skill of candidate

        :return:
             html styled string with a certain candidate's data
             or info that candidate isn't found
            """

        skill_name = skill_name.lower()
        candidates_by_skill = ''

        for candidate in self.candidates:

            # searching skill in string of skills turned into a list
            if skill_name in candidate.get('skills', '').lower().split(', '):

                name = f"Имя кандидата: {candidate.get('name', '')}"
                position = f"Позиция: {candidate.get('position', '')}"
                skills = f"Навыки: {candidate.get('skills', '')}" + '\n'

                # preparing a string with candidates' data'
                candidates_by_skill += \
                    '\n'.join((name, position, skills)) + '\n'

        return f'<pre>{candidates_by_skill}</pre>' \
            if candidates_by_skill else 'Подходящих кандидатов не найдено'

    def set_rules(self):
        """This method prepares routes for Flask instance"""
        self.app.add_url_rule('/', view_func=self.get_all)
        self.app.add_url_rule('/candidates/<int:pk>',
                              view_func=self.get_by_pk)
        self.app.add_url_rule('/skills/<skill_name>',
                              view_func=self.get_by_skill)

    def run_app(self):
        """Running Flask app"""
        self.app.run()

    def __repr__(self):

        return f'CandidateFinder - Flask app returning candidates data'
