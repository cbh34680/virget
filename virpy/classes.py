import sys

class Command:
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        raise NotImplementedError()


class ObjectNotFoundError(Exception):
    pass

