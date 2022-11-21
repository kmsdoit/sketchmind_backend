from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI
from app.common.config import conf
from dataclasses import asdict
from app.database.conn import db
from app.router import index, auth


def create_app():
    c = conf()
    app = FastAPI()
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)

    # database initialize

    # redis initiallize

    # middleware

    # router
    app.include_router(index.router)
    app.include_router(auth.router, tags=["Authentication"], prefix="/api")
    # app.include_router(auth.router, tags=["Authentication"], prefix="/api")

    return app


app = create_app()

print(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
