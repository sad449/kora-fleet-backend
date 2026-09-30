from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlmodel import Session, select, func, or_
from fastapi import HTTPException, status
from app.models.vehicle import Vehicle
from app.models.vehicle_assignment import VehicleAssignment


def get_vehicle(vehicle_id: int, session: Session) -> Vehicle:
    """Get a single vehicle by ID"""
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    return vehicle


def get_vehicle_by_registration(registration_number: str, session: Session) -> Optional[Vehicle]:
    """Get a vehicle by registration number"""
    return session.exec(
        select(Vehicle).where(Vehicle.registration_number == registration_number)
    ).first()


def get_vehicle_by_license_plate(license_plate: str, session: Session) -> Optional[Vehicle]:
    """Get a vehicle by license plate number"""
    return session.exec(
        select(Vehicle).where(Vehicle.license_plate == license_plate)
    ).first()


def get_vehicles(
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
) -> Dict[str, Any]:
    """
    Get list of vehicles with optional filters and pagination
    """
    query = select(Vehicle)
    count_query = select(func.count()).select_from(Vehicle)

    # applying the filters
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Vehicle.registration_number.ilike(search_term),
                Vehicle.make.ilike(search_term),
                Vehicle.model.ilike(search_term),
                Vehicle.license_plate.ilike(search_term)
            )
        )
        count_query = count_query.where(
            or_(
                Vehicle.registration_number.ilike(search_term),
                Vehicle.make.ilike(search_term),
                Vehicle.model.ilike(search_term),
                Vehicle.license_plate.ilike(search_term)
            )
        )

    if status:
        query = query.where(Vehicle.status == status)
        count_query = count_query.where(Vehicle.status == status)

    if make:
        query = query.where(Vehicle.make.ilike(f"%{make}%"))
        count_query = count_query.where(Vehicle.make.ilike(f"%{make}%"))

    if model:
        query = query.where(Vehicle.model.ilike(f"%{model}%"))
        count_query = count_query.where(Vehicle.model.ilike(f"%{model}%"))

    if year:
        query = query.where(Vehicle.year == year)
        count_query = count_query.where(Vehicle.year == year)

    if is_active is not None:
        query = query.where(Vehicle.is_active == is_active)
        count_query = count_query.where(Vehicle.is_active == is_active)

    if not include_deleted:
        query = query.where(Vehicle.deleted_at.is_(None))
        count_query = count_query.where(Vehicle.deleted_at.is_(None))

    # All count
    total = session.exec(count_query).first()

    # paginated results
    query = query.offset(skip).limit(limit).order_by(Vehicle.created_at.desc())
    vehicles = session.exec(query).all()

    return {
        "items": vehicles,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "size": limit,
        "pages": (total + limit - 1) // limit if limit > 0 else 1
    }


def create_vehicle(
    vehicle_data: Dict[str, Any],
    session: Session,
    current_user_id: int
) -> Vehicle:
    """Create a new vehicle"""
    
    # Check if registration number already exists
    existing = get_vehicle_by_registration(vehicle_data["registration_number"], session)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this registration number already exists"
        )
    
    # Check if license plate already exists
    existing_plate = get_vehicle_by_license_plate(vehicle_data["license_plate"], session)
    if existing_plate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with this license plate already exists"
        )
    
    # Create new vehicle
    vehicle = Vehicle(
        **vehicle_data,
        created_by=current_user_id,
        created_at=datetime.utcnow()
    )
    
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    return vehicle


def update_vehicle(
    vehicle_id: int,
    vehicle_data: Dict[str, Any],
    session: Session,
    current_user_id: int
) -> Vehicle:
    """Update an existing vehicle"""
    # first check the vehicle to update exists
    vehicle = get_vehicle(vehicle_id, session)
    
    # If updating registration number, check uniqueness
    if "registration_number" in vehicle_data and vehicle_data["registration_number"] != vehicle.registration_number:
        existing = get_vehicle_by_registration(vehicle_data["registration_number"], session)
        if existing and existing.id != vehicle_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle with this registration number already exists"
            )
    
    # If updating license plate, check uniqueness
    if "license_plate" in vehicle_data and vehicle_data["license_plate"] != vehicle.license_plate:
        existing_plate = get_vehicle_by_license_plate(vehicle_data["license_plate"], session)
        if existing_plate and existing_plate.id != vehicle_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vehicle with this license plate already exists"
            )
    
    # Update fields
    for key, value in vehicle_data.items():
        if value is not None:
            setattr(vehicle, key, value)
    
    vehicle.updated_at = datetime.utcnow()
    vehicle.updated_by = current_user_id
    
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    return vehicle


def update_vehicle_status(
    vehicle_id: int,
    status: str,
    session: Session,
    current_user_id: int,
    notes: Optional[str] = None
) -> Vehicle:
    """Update vehicle status only"""
    
    vehicle = get_vehicle(vehicle_id, session)
    if status in ["available", "retired"] and vehicle.status == "assigned":
        # Check if there are active assignments
        active_assignment = session.exec(
            select(VehicleAssignment).where(
                VehicleAssignment.vehicle_id == vehicle_id,
                VehicleAssignment.assigned_to.is_(None)
            )
        ).first()
        
        if active_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change status of a vehicle with active assignments. Please end the assignment first."
            )
    
    vehicle.status = status
    if notes:
        vehicle.notes = notes
    
    vehicle.updated_at = datetime.utcnow()
    vehicle.updated_by = current_user_id
    
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    return vehicle


def delete_vehicle(
    vehicle_id: int,
    session: Session,
    current_user_id: int,
    permanent: bool = False
) -> None:
    """
    Delete or soft delete a vehicle
    """
    vehicle = get_vehicle(vehicle_id, session)
    
    # Check if vehicle has active assignments
    active_assignment = session.exec(
        select(VehicleAssignment).where(
            VehicleAssignment.vehicle_id == vehicle_id,
            VehicleAssignment.assigned_to.is_(None)
        )
    ).first()
    
    if active_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a vehicle with active assignments. Please end the assignment first."
        )
    
    if permanent:
        # Hard delete
        session.delete(vehicle)
    else:
        # Soft delete
        vehicle.is_active = False
        vehicle.is_deleted = True
        vehicle.deleted_at = datetime.utcnow()
        vehicle.deleted_by = current_user_id
        session.add(vehicle)
    
    session.commit()


def restore_vehicle(
    vehicle_id: int,
    session: Session,
    current_user_id: int
) -> Vehicle:
    """Restore a soft-deleted vehicle"""
    
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )
    
    if not vehicle.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle is not deleted"
        )
    
    vehicle.is_active = True
    vehicle.deleted_at = None
    vehicle.deleted_by = None
    vehicle.updated_at = datetime.utcnow()
    vehicle.updated_by = current_user_id
    
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    
    return vehicle


def get_available_vehicles(
    session: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Vehicle]:
    """Get all available vehicles (not assigned)"""
    # Get vehicles that are available
    available_vehicles = session.exec(
        select(Vehicle).where(
            Vehicle.status == "available",
            Vehicle.is_active == True,
            Vehicle.deleted_at.is_(None)
        ).offset(skip).limit(limit)
    ).all()
    
    # Filter out vehicles that have active assignments
    result = []
    for vehicle in available_vehicles:
        active_assignment = session.exec(
            select(VehicleAssignment).where(
                VehicleAssignment.vehicle_id == vehicle.id,
                VehicleAssignment.assigned_to.is_(None)
            )
        ).first()
        
        if not active_assignment:
            result.append(vehicle)
    
    return result


def get_vehicle_maintenance_history(
    vehicle_id: int,
    session: Session
) -> Dict[str, Any]:
    """Get maintenance and assignment history for a vehicle"""
    vehicle = get_vehicle(vehicle_id, session)
    
    # Get all assignments for this vehicle
    assignments = session.exec(
        select(VehicleAssignment).where(
            VehicleAssignment.vehicle_id == vehicle_id
        ).order_by(VehicleAssignment.assigned_from.desc())
    ).all()
    
    return {
        "vehicle": vehicle,
        "total_assignments": len(assignments),
        "active_assignments": len([a for a in assignments if a.assigned_to is None]),
        "assignments": assignments
    }