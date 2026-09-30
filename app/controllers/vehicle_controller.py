from typing import Optional, Dict, Any
from sqlmodel import Session
from fastapi import HTTPException, status
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleListResponse,
    VehicleStatusUpdate
)
from app.services import vehicle_service as service


def create_vehicle_controller(
    vehicle_data: VehicleCreate,
    session: Session,
    current_user_id: int
) -> VehicleResponse:
    """Controller for creating a vehicle"""
    result = service.create_vehicle(
        vehicle_data=vehicle_data.model_dump(exclude_unset=True),
        session=session,
        current_user_id=current_user_id
    )
    return VehicleResponse.model_validate(result)


def get_vehicle_controller(
    vehicle_id: int,
    session: Session
) -> VehicleResponse:
    """Controller for getting a single vehicle"""
    result = service.get_vehicle(vehicle_id, session)
    return VehicleResponse.model_validate(result)


def get_vehicles_controller(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    status: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    year: Optional[int] = None,
    is_active: Optional[bool] = None,
    include_deleted: bool = False
) -> VehicleListResponse:
    """Controller for getting list of vehicles"""
    result = service.get_vehicles(
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
    return VehicleListResponse(
        items=[VehicleResponse.model_validate(item) for item in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"]
    )


def update_vehicle_controller(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    session: Session,
    current_user_id: int
) -> VehicleResponse:
    """Controller for updating a vehicle"""
    result = service.update_vehicle(
        vehicle_id=vehicle_id,
        vehicle_data=vehicle_data.model_dump(exclude_unset=True),
        session=session,
        current_user_id=current_user_id
    )
    return VehicleResponse.model_validate(result)


def update_vehicle_status_controller(
    vehicle_id: int,
    status_data: VehicleStatusUpdate,
    session: Session,
    current_user_id: int
) -> VehicleResponse:
    """Controller for updating vehicle status"""
    result = service.update_vehicle_status(
        vehicle_id=vehicle_id,
        status=status_data.status,
        session=session,
        current_user_id=current_user_id,
        notes=status_data.notes
    )
    return VehicleResponse.model_validate(result)


def delete_vehicle_controller(
    vehicle_id: int,
    session: Session,
    current_user_id: int,
    permanent: bool = False
) -> Dict[str, str]:
    """Controller for deleting a vehicle"""
    service.delete_vehicle(
        vehicle_id=vehicle_id,
        session=session,
        current_user_id=current_user_id,
        permanent=permanent
    )
    message = "Vehicle deleted permanently" if permanent else "Vehicle deleted successfully"
    return {"message": message}


def restore_vehicle_controller(
    vehicle_id: int,
    session: Session,
    current_user_id: int
) -> VehicleResponse:
    """Controller for restoring a soft-deleted vehicle"""
    result = service.restore_vehicle(
        vehicle_id=vehicle_id,
        session=session,
        current_user_id=current_user_id
    )
    return VehicleResponse.model_validate(result)


def get_available_vehicles_controller(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> list[VehicleResponse]:
    """Controller for getting available vehicles"""
    results = service.get_available_vehicles(
        session=session,
        skip=skip,
        limit=limit
    )
    return [VehicleResponse.model_validate(item) for item in results]


def get_vehicle_maintenance_history_controller(
    vehicle_id: int,
    session: Session
) -> Dict[str, Any]:
    """Controller for getting vehicle maintenance history"""
    return service.get_vehicle_maintenance_history(vehicle_id, session)