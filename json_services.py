import json


class JSONServices:
    @staticmethod
    def load(filename: str):
        try:
            with open(filename) as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found.")
