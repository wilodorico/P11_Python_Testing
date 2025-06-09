import uuid


class Competition:
    def __init__(self, name: str, date: str, available_places: int):
        self.id = uuid.uuid4()
        self.name = name
        self.date = date
        self.available_places = available_places

    def __str__(self) -> str:
        return (
            f"Competition(id={self.id}, name={self.name}, date={self.date}, available_places={self.available_places})"
        )
