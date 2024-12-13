from datetime import datetime


class CreatedAtMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class TestClass(metaclass=CreatedAtMeta):
    pass


if __name__ == '__main__':
    print(TestClass.created_at)