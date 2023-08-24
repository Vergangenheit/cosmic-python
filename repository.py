import abc
from domain.model import Batch
from typing import List
from sqlalchemy.orm import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> Batch:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Batch]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: Batch):
        self.session.add(batch)

    def get(self, reference: str) -> Batch:
        return self.session.query(Batch).filter_by(reference=reference).one()

    def list(self) -> List[Batch]:
        return self.session.query(Batch).all()
