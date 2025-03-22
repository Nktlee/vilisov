import sys
from pathlib import Path
import logging

from fastapi import FastAPI
import uvicorn

from api.tasks import router as router_task

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)


app = FastAPI()

app.include_router(router_task)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
