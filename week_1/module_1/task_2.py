from typing import Callable


def access_control(roles) -> Callable:
    valid_roles = ['admin', 'moderator']

    def decorator(func):

        def wrapper(*args, **kwargs):
            for role in roles:
                if role in valid_roles:
                    result = func(*args, **kwargs)
                    return result
            
            raise PermissionError('Access denied')
        return wrapper
    
    return decorator


@access_control(roles=['moderator'])
def access_test() -> None:
    print('Access allowed')


if __name__ == '__main__':
    access_test()