import json


class JSONServices:
    @staticmethod
    def load(filename: str):
        with open(filename) as file:
            return json.load(file)
