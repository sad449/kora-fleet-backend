# this is the FastAPI app. it wires up middleware and routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health

app = FastAPI(title="Kora Fleet API")
# this allows the React dev server (currenlty running on port 5173) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# all routes live under '/ap'.
app.include_router(health.router, prefix="/api")