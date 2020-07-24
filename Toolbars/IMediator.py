from abc import abstractmethod


class IMediator:
    @abstractmethod
    def dispatch(self, comp, event: str):
        pass
