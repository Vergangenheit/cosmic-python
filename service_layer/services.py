from __future__ import annotations

from domain import model
from domain.model import OrderLine, Batch
from typing import List, Optional
from datetime import date
from repository import AbstractRepository
from sqlalchemy.orm import Session


class InvalidSku(Exception):
    pass


def is_valid_sku(sku: str, batches: List[Batch]):
    return sku in {b.sku for b in batches}


def allocate(orderid: str, sku: str, qty: int, repo: AbstractRepository, session: Session) -> str:
    line = OrderLine(orderid, sku, qty)
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session: Session) -> None:
    repo.add(Batch(ref, sku, qty, eta))
    session.commit()
