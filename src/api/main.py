from fastapi import FastAPI

from src.api.routers.users import router as users_router
from src.api.routers.sets import router as sets_router
from src.api.routers.colours import router as colours_router
from src.api.routers.health import router as health_router

app = FastAPI(
    title="LEGO Brick Manager",
    description="API for managing LEGO brick inventories and sets",
    version="1.0.0"
)

# Register routers
app.include_router(health_router)
app.include_router(users_router)
app.include_router(sets_router)
app.include_router(colours_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
