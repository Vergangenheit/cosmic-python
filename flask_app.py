from typing import List

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import config
import model
import orm
import repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session: Session = get_session()
    batches: List[model.Batch] = repository.SqlRepository(session).list()
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )
    batchref: str = model.allocate(line, batches)

    return {"batchref", batchref}, 201
