Validol2
========

Useful GET/POST-parameters or JSON parsing* and validation tool.

 * It doesn't actually parse textual data. It operates on python data structures.


Why
---
 * Checks that supplied data is valid
 * Automatically converts types for you
 * Very extensible
 * License that gives you unlimited usage scenarios :-)

Usage
-----
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

Tips on testing
---------------
    python validol2.py

If nothing is printed then tests pass.

Credits
-------
 * [Konstantin Merenkov](http://kmerenkov.ru/)

License
-------
See LICENSE file.
Long story short: WTFPL v2

