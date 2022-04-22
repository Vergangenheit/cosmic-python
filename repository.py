import abc
from typing import List

from sqlalchemy.orm import Session

import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference):
        raise NotImplementedError

class SqlRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: model.Batch):
        self.session.add(batch)

    def get(self, reference) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self) -> List[model.Batch]:
        return self.session.query(model.Batch).all()
