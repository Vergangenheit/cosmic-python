from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain import model
from src.domain.model import OrderLine, Batch
from src.adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass


def is_valid_sku(sku: str, batches: List[Batch]) -> bool:
    return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: AbstractRepository, session: Session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], repo: AbstractRepository, session: Session):
    repo.add(Batch(ref=ref, sku=sku, qty=qty, eta=eta))


def deallocate(line: OrderLine, batch: Batch, session: Session) -> Optional[str]:
    if line.sku != batch.sku:
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.deallocate(line, batch)
    session.commit()
    return batchref

