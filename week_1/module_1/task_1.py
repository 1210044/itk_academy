from typing import Callable
import unittest.mock


cache = {}


def lru_cache(*func, **params) -> Callable:
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (func, *args, *kwargs.values())
            if cache.get(key):
                return cache[key]
            
            result = func(*args, **kwargs)
            max_size = params.get('maxsize')
            if max_size:
                while len(cache) >= max_size:
                    first_key = next(iter(cache.keys()))
                    del cache[first_key]
            
            cache[key] = result
            return result
        return wrapper
    
    if func and isinstance(func[0], Callable):
        return decorator(func[0])
    return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12
    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4