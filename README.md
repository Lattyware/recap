recap
=====

`recap` is a tiny library designed to provide a solid implementation of the
mark and recapture pattern.

The simplest way to understand what it's for and how to use it is to take a
look at [the example](example.py).

The problem
-----------

It is semantically pleasing to use decorators to 'register' functions - for
example, if you have a GUI toolkit where whenever someone presses a button, a
function should be called, it reads nicely to have a decorator that registers
the function as a callback for a given event and widget:

```python
@callback(widget, signal)
def do_something():
    ...
```

However, this falls apart when you try and use it within classes - the functions
are decorated when they are declared, as unbound functions. When you try and
call such a function, it will fail, expecting to be bound so it receives an
instance as the first argument.

```python
class SomeClass:
    @callback(widget, signal)  # The callback will get the unbound method!
    def do_something(self):    # Expect to see "missing 1 required positional
        ...                    # argument: 'self'".
```

The solution
------------

The mark and recapture pattern works by marking the functions rather than
registering them straight away. Then, when an instance is created, the methods
are recaptured and registered. As they are bound at this point, everything works
as expected.

Recap does this all for you - you just add a class decorator, and then use mark
instead of your original decorator.

```python
@recapture(callback)  # Pass your existing decorator here!
class SomeClass:
    @mark(widget, signal)  # Then replace calls to your decorator with `mark()`.
    def do_something(self):
        ...
```

About
-----

recap is a tiny library, and it's MIT Licensed - feel free to embed it into your
software projects as needed.

recap has been tested in Python 2.7 and 3.3.