from fastapi import APIRouter


auth_router = APIRouter()


@auth_router.post("/signup")
def create_account():
    pass


@auth_router.post("/login")
def login():
    pass
