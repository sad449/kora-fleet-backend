from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from app.database import get_session
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleListResponse,
    VehicleStatusUpdate
)
from app.controllers import vehicle_controller as controller

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    vehicle: VehicleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new vehicle"""
    return controller.create_vehicle_controller(
        vehicle,
        session,
        current_user.id
    )


@router.get("/", response_model=VehicleListResponse)
def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    status: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None,
    is_active: Optional[bool] = True,
    include_deleted: bool = False,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all vehicles with optional filters"""
    return controller.get_vehicles_controller(
        session=session,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        make=make,
        model=model,
        year=year,
        is_active=is_active,
        include_deleted=include_deleted
    )


@router.get("/available", response_model=list[VehicleResponse])
def get_available_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all available vehicles (not assigned)"""
    return controller.get_available_vehicles_controller(
        session=session,
        skip=skip,
        limit=limit
    )


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific vehicle by ID"""
    return controller.get_vehicle_controller(vehicle_id, session)


@router.get("/{vehicle_id}/history", response_model=dict)
def get_vehicle_history(
    vehicle_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get vehicle assignment and maintenance history"""
    return controller.get_vehicle_maintenance_history_controller(vehicle_id, session)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a vehicle"""
    return controller.update_vehicle_controller(
        vehicle_id,
        vehicle,
        session,
        current_user.id
    )


@router.patch("/{vehicle_id}/status", response_model=VehicleResponse)
def update_vehicle_status(
    vehicle_id: int,
    status_data: VehicleStatusUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update vehicle status"""
    return controller.update_vehicle_status_controller(
        vehicle_id,
        status_data,
        session,
        current_user.id
    )


@router.delete("/{vehicle_id}", status_code=status.HTTP_200_OK)
def delete_vehicle(
    vehicle_id: int,
    permanent: bool = Query(False, description="Permanently delete the vehicle"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a vehicle (soft delete by default)"""
    return controller.delete_vehicle_controller(
        vehicle_id,
        session,
        current_user.id,
        permanent
    )


@router.post("/{vehicle_id}/restore", response_model=VehicleResponse)
def restore_vehicle(
    vehicle_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Restore a soft-deleted vehicle"""
    return controller.restore_vehicle_controller(
        vehicle_id,
        session,
        current_user.id
    )