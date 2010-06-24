# -*- coding: utf-8 -*-

#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2010 Konstantin Merenkov <kmerenkov@gmail.com>
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
from itertools import izip, cycle


__version__ = '0.1'
__author__  = "Konstantin Merenkov <kmerenkov@gmail.com>"


class ValidationError(Exception):
    def __init__(self, message):
        super(ValidationError, self).__init__(message)


def validate(scheme, obj):
    """
    >>> validate(str, "foo")
    'foo'
    >>> validate(int, 10)
    10
    >>> validate(int, "10")
    10
    >>> validate([int], ["10"])
    [10]
    >>> validate(sequence([int]), xrange(10))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> validate({"user": str,
    ...           "blocked": boolean,
    ...           "email": str},
    ...          {"user": "john",
    ...           "blocked": "false",
    ...           "email": "john@example.com"}
    ...          )
    {'blocked': False, 'email': 'john@example.com', 'user': 'john'}
    >>> validate(any_of([10, 20, 30]), 10)
    10
    >>> try:
    ...    validate(any_of([10, 20, 30]), 40)
    ... except ValidationError, e:
    ...    print str(e)
    Failed any_of validation: 40
    >>> validate(in_range(0, 10), 5)
    5
    >>> try:
    ...    validate(in_range(0, 10), 15)
    ... except ValidationError, e:
    ...    print str(e)
    Failed in_range validation: 15
    """
    if callable(scheme):
        return scheme(obj)
    elif hasattr(scheme, 'items') and hasattr(scheme, 'items'):
        return validate_dict(scheme, obj)
    elif hasattr(scheme, '__iter__') and hasattr(obj, '__iter__'):
            return validate_iterable(scheme, obj)
    elif scheme == obj:
        return obj
    raise ValidationError("Don't know how to validate %s against %s" % (obj, scheme))

# special validators
def boolean(obj):
    if type(obj) is bool:
        return obj
    ol = str(obj).lower()
    if ol in ["1", "true"]:
        return True
    elif ol in ["0", "false"]:
        return False
    raise ValidationError("Failed bool validation: %s" % (obj,))

def in_range(start, end):
    def _in_range(obj):
        ok = False
        try:
            ok = start <= float(obj) <= end
        except Exception:
            pass
        if not ok:
            raise ValidationError("Failed in_range validation: %s" % (obj,))
        return obj
    return _in_range

def sequence(scheme):
    def _sequence(obj):
        return validate_iterable(cycle(scheme), obj)
    return _sequence

def str_strict(obj):
    if isinstance(obj, basestring):
        return obj
    raise ValidationError("Failed str_strict validation: %s" % (obj,))

def any_of(xs):
    def _any_of(obj):
        for x in xs:
            try:
                return validate(x, obj)
            except:
                pass
            raise ValidationError("Failed any_of validation: %s" % (obj,))
        return result
    return _any_of


# actual implementation

def validate_iterable(scheme, obj):
    results = []
    for s, o in izip(scheme, obj):
        try:
            results.append(validate(s, o))
        except (TypeError, ValueError):
            raise ValidationError("Failed iterable validation: %s" % (obj,))
    return results

def validate_dict(scheme, obj):
    if len(scheme) != len(obj):
        raise ValidationError("Failed dict validation: %s" % (obj,))
    validated = {}
    scheme_dict = dict(scheme)
    for okey, ovalue in obj.items():
        ok = False
        for skey, svalue in scheme_dict.items():
            try:
                k = validate(skey, okey)
                v = validate(svalue, ovalue)
                validated[k] = v
                ok = True
                scheme_dict.pop(skey)
                break
            except Exception:
                pass
        if not ok:
            raise ValidationError("Failed dict validation: %s" % ((okey, ovalue),))
    return validated


if __name__ == '__main__':
    import doctest
    doctest.testmod()
