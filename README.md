Validol2
========

Useful GET/POST-parameters or JSON parsing* and validation tool.

 * It doesn't actually parse textual data. It operates on python data structures.

Why
---
 * Checks that supplied data is valid (supports optional keys in dictionaries)
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

Too long/didn't read
--------------------

Imagine that you expect a GET request of the following form:
    {"page": "10"}

On server-side you need to check that the only supplied parameter is "page",
that its value is an integer and it is greater than zero (negative pages are
weird).

Here's how validol2 helps you:
    >>> validate({"page": gt(0)}, # so-called scheme
                 {"page": "10"}) # the GET-request
    {"page": 10}

As you can see, you got back data from the GET-request, but 10 is not
a string anymore. More than that, it is checked to be greater than zero!

What's going on here?

#### Scheme
Scheme is a pattern for data you expect. It is used for both validation and
type conversion.

Breakdown of `{"page": gt(0)}`:

  1. {...} - means that we expect a dictionary
  2. "page": ... - means that we expect only one key with value "page"
  3. gt(0) - means that we expect an numeric which is greater than zero (also conversion to integer happens here)


#### Extensibility

Forgot to mention that validol2 is very extensible!
For example:
    from validol2 import validate, ValidationError
    
    
    def upper_case(expected):
        def _upper_case(value):
            if value == expected
                return value
            raise ValidationError("Expected %s to be upper case!" % (value,))
        return _upper_case
    
    print validate(upper_case(str), "FOO") # will print FOO
    print validate(upper_case(str), "foo") # will raise an exception

That's the only effort you need to extend validol2.


PS Yes, you can think of validol2 as of forms without forms.

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

