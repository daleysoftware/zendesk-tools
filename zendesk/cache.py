import abc

class AbstractObjectCacher:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.data = None

    def _cache(self, data):
        self.data = data
    def _get(self):
        if self.data is None: self._process()
        return self.data

    @abc.abstractmethod
    def _process(self):
        return