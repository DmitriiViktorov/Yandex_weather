import uvicorn
from fastapi import FastAPI
from app.services.db import Base, engine
from app.routes import all_routes

app = FastAPI()
app.include_router(all_routes)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

