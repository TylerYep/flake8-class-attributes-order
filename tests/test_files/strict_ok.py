class Foo:
    class Meta:
        a = 3

    CONSTANT = True

    def __init__():  # pylint: disable=no-method-argument
        ...

    @property
    def bar(self):
        ...

    @property
    def _bar(self):
        ...

    @staticmethod
    def egg():
        ...

    @staticmethod
    def _egg():
        ...

    @classmethod
    def foobar(cls):
        ...

    @classmethod
    def _foobar(cls):
        ...
