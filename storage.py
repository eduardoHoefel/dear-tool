
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#Python3
class Storage(metaclass=Singleton):

    def __init__(self):
        self.data = {}

    def get(self, item):
        return self.data[item] if item in self.data else None

    def set(self, item, value):
        self.data[item] = value

    def __str__(self):
        return str(self.data)
