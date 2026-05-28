from fastapi import FastAPI
from .routers import org_router
from .routers import task_router, team_router
from .routers import auth_router, user_router
from .routers import proj_router, label_router
from .routers import milestone_router, activity_router


app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(org_router)
app.include_router(team_router)
app.include_router(proj_router)
app.include_router(task_router)
app.include_router(label_router)
app.include_router(milestone_router)
app.include_router(activity_router)

 
