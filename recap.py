#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Recap allows you to easily use decorators to provide callbacks to methods.

Decorators are bound at definition time - they work on functions, not methods.
Decorators are normally great for assigning functions as callbacks - it reads
well. However, because of the aforementioned methodology, this doesn't work for
methods. Recap uses the mark and recapture method by marking the function with
a decorator, then assigning it to the callback when the class is
instantiated."""

from functools import wraps
import inspect


def recapture(handler):
    """A class decorator that recaptures marked functions when they become
    methods on an instantiated object. Takes one argument - the function used
    to handle the marks upon recapture.

    The functions will receive the arguments given to the `mark()` decorator
    when the method was marked. It should then return a function that takes the
    marked function and handles it. This may sound convoluted, but what this
    means is that the handler should be a decorator - allowing you to use the
    same function to decorate functions and as a handler for methods being
    recaptured. If this isn't clear - take a look at the example.
    """
    def decorate(cls):
        init = cls.__init__
        @wraps(init)
        def wrapper(instance, *args, **kwargs):
            handle(instance, handler)
            return init(instance, *args, **kwargs)
        cls.__init__ = wrapper
        return cls
    return decorate


def handle(instance, handler):
    """Apply the given handler to any marked methods on instance. Generally the
    best way to do this is by using the recapture decorator, rather than calling
    this directly.

    instance is the instance to be checked for marked methods, and handler is
    the decorator applied to the functions (note that while the handler should
    function like a decorator, it does not assign back to the function).
    """
    for name, method in inspect.getmembers(instance, inspect.ismethod):
        try:
            markings = method.__func__._markings
        except AttributeError:
            continue
        for marking in markings:
            handler(*marking)(method)


def mark(*args):
    """A decorator that marks the method for recapture later. This will cause
    the handler to be run with the arguments given when a class is
    instantiated.
    """
    def decorate(f):
        try:
            f._markings.add(args)
        except AttributeError:
            f._markings = {args}
        return f
    return decorate