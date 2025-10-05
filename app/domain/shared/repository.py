from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")

class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def list(self) -> List[T]:
        pass

    @abstractmethod
    async def add(self, obj: T) -> None:
        pass

    @abstractmethod
    async def update(self, obj: T) -> None:
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        pass