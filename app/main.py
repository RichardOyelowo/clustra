from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routers import (
    activity_router,
    auth_router,
    label_router,
    milestone_router,
    org_router,
    proj_router,
    task_router,
    team_router,
    user_router,
)

app = FastAPI()


# serve static & html Files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/login.html")

@app.get("/{page}.html")
async def serve_page(page: str):
    return FileResponse(f"frontend/{page}.html")


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(org_router)
app.include_router(team_router)
app.include_router(proj_router)
app.include_router(task_router)
app.include_router(label_router)
app.include_router(milestone_router)
app.include_router(activity_router)
