class Foo:
    CONSTANT = 42

    def bar():  # pylint: disable=no-method-argument, no-self-use
        ...

    """Oh, really?"""  # pylint: disable=pointless-string-statement
