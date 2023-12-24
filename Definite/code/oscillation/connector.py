import abc

class Connector(abc.ABC):

    @abc.abstractmethod
    def force(self):
        pass
    
    @abc.abstractmethod
    def update(self):
        pass