from abc import abstractmethod


class IMediator:
    @abstractmethod
    def dispatch(self, comp, val, notify: bool):
        pass
