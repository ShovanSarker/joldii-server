import uuid

__author__ = 'exor'


class UUID:
    
    def __init__(self):
        pass

    @staticmethod
    def uuid_generator():
        return str(uuid.uuid4())
