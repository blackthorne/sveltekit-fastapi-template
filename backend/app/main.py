"""FastAPI application entrypoint.

Run with:  uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .auth import CurrentUser, create_access_token
from .config import settings
from .models import Token, UserCreate, UserLogin, UserPublic
from .users import create_user, get_user, seed_demo_user, verify_password


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_demo_user()
    yield


app = FastAPI(title="SvelteKit + FastAPI template", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------- auth ----


@app.post("/auth/register", response_model=UserPublic, status_code=201)
def register(body: UserCreate):
    if get_user(body.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken"
        )
    user = create_user(body.username, body.password)
    return UserPublic(username=user["username"], is_active=user["is_active"])


@app.post("/auth/login", response_model=Token)
def login(body: UserLogin):
    user = get_user(body.username)
    if user is None or not verify_password(body.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return Token(access_token=create_access_token(user["username"]))


# --------------------------------------------------------------- users ----


@app.get("/users/me", response_model=UserPublic)
def read_me(user: CurrentUser):
    return UserPublic(username=user["username"], is_active=user["is_active"])


# ----------------------------------------------------------- protected ----


@app.get("/protected/ping")
def protected_ping(user: CurrentUser):
    return {"message": f"hello {user['username']}, your JWT is valid"}


# -------------------------------------------------------------- public ----


@app.get("/health")
def health():
    return {"status": "ok"}
