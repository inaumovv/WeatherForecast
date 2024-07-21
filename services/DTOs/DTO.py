import json

from django.db.models import Model

from services.has_attributes import HasAttributes


class DTO(HasAttributes):
    def __init__(self, data: dict | Model | None):
        if isinstance(data, Model):
            data = data.__dict__

        if data:
            self.set_attributes(data)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        dictionary = self.__dict__

        for key, item in dictionary.items():
            if isinstance(item, DTO):
                dictionary[key] = item.to_dict()

            elif isinstance(item, Model):
                dictionary[key] = item.__dict__

        return dictionary


