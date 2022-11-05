import time
from typing import List, Optional

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, Session

from src import config
from src.adapters.orm import metadata
from src.domain import model
from src.service_layer import services
from src.domain.model import Batch
from src.adapters import repository, orm

# orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


def is_valid_sku(sku: str, batches: List[Batch]) -> bool:
    return sku in {b.sku for b in batches}


@app.route("/create_db", methods=["GET"])
def create_db():
    if request.method == "GET":
        orm.start_mappers()
        return {"message": "tables created"}, 200


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return {"message": "welcome to cosmic python api"}, 200


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session: Session = get_session()
    repo = repository.SqlRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )
    try:
        batchref: str = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    session.commit()
    return {"batchref", batchref}, 201
