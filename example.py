from recap import mark, recapture

"""Example usage of recap."""

# This represents some GUI library, registering the method with an event.
callbacks = {}

# A decorator that registers callbacks with our GUI library.
def register_callback(widget, event):
    def decorate(function):
        callbacks[widget, event] = function
        return function
    return decorate


@register_callback("Key", "Down")
def test():
    print("Test function!")

@recapture(register_callback)
class Test:
    def __init__(self, value):
        self.value = value

    @mark("Button", "Click")
    def test(self):
        print("Test method!")
        print(self.value)

    @register_callback("Key", "Up")
    def broken(self):
        print("This won't work")
        print(self.value)


Test("Test Object")

# The user presses a key.
callbacks["Key", "Down"]()
# This works, calling the function.

# The user clicks the button.
callbacks["Button", "Click"]()
# This works, calling the method.

# The user releases a key.
callbacks["Key", "Up"]()
# This doesn't work - the decorator registers the unbound function, not the
# bound method.