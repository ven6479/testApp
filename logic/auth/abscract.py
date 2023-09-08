from abc import ABC, abstractmethod


class Authenticator(ABC):

    @abstractmethod
    async def authenticate(self) -> dict:
        pass
