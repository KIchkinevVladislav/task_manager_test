import uvicorn
from fastapi import FastAPI

from app.api import task_router
from app.middleware import handle_api_exceptions

app = FastAPI()

app.middleware("http")(handle_api_exceptions)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
