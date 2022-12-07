from collections import deque
from functools import partial
from itertools import islice
from typing import Sequence

l = [1,2,3,4,5,6] # [[1,2,3],[4,5,6],[7]]
e = []
_marker = object()

def take(iterable, n):
    return list(islice(iterable, n))

def chunked(iterable, n, strict=False):
    iterator = iter(partial(take, iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError('n cant be None when strict is True')
        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError('iterator is not divisible by n')
                yield chunk
        return iter(ret())
    else:
        return iterator

# print(list(chunked(l, 3, strict=True)))

def first(iterable, default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default is _marker:
            raise ValueError('first() was called on an empty iterable, and no '
            'default value was provided.') from e
        return default
    
# print(first(e))

def last(iterable, default=_marker):
    try:
        if isinstance(iterable,Sequence):
            return iterable[-1]
        elif hasattr(iterable, '__reversed__'):
            return next(reversed(iterable))
        else:
            return deque(iterable, maxlen=1)[-1]
    except (IndexError, TypeError, StopIteration):
        if default is _marker:
            raise ValueError(
                'last() was called on an empty iterable, and no default was provided.'
            )
        return default

# print(last(l))

def nth_or_last(iterable, n, default=_marker):
    return last(islice(iterable, n+1), default=default)

print(nth_or_last(l, 4))
