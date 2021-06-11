from abc import ABC, abstractmethod


class ClassMediator(ABC):

    @abstractmethod
    def __init__(self, atdx_core):
        self.atdx = atdx_core

    @abstractmethod
    def notify(self, sender, event):
        pass
