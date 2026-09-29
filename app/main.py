from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, auth,vehicle_routes

app = FastAPI(title="Kora Fleet API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")
# app.include_router(users.router, prefix="/api/users")
# app.include_router(roles.router, prefix="/api/roles")
app.include_router(vehicle_routes.router, prefix="/api/vehicles")