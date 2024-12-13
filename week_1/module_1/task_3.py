from singleton import singleton_import


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    

class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, value):
        if not hasattr(self, 'initialized'):
            self.value = value
            self.initialized = True


if __name__ == '__main__':
    singleton_1 = Singleton(10)
    singleton_2 = Singleton(20)

    print(singleton_1.value)
    print(singleton_2.value)
    print(singleton_import.value)