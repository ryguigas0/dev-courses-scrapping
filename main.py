from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from models import create_database
from controllers import routers
import uvicorn

# Creates the database tables
create_database()

# Create REST API
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

for r in routers:
    app.include_router(r)

if __name__ == "__main__":
    uvicorn.run("main:app", port=3000, reload=True)
