from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db import models
from app.schemas import result as result_schemas
from app.api.dependencies import get_user_by_id

router = APIRouter()


@router.post("/", response_model=result_schemas.LabResult, status_code=status.HTTP_201_CREATED)
def create_lab_result(
    *,
    db: Session = Depends(get_db),
    result_in: result_schemas.LabResultCreate,
) -> Any:
    """
    Create a new lab result
    """
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == result_in.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {result_in.user_id} not found",
        )
    
    # Create new lab result
    result = models.LabResult(
        user_id=result_in.user_id,
        test_name=result_in.test_name,
        test_date=result_in.test_date,
        result_value=result_in.result_value,
        normal_range=result_in.normal_range,
        unit=result_in.unit,
        notes=result_in.notes,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get("/", response_model=List[result_schemas.LabResult])
def read_lab_results(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve lab results for all users
    """
    results = db.query(models.LabResult).offset(skip).limit(limit).all()
    return results


@router.get("/user/{user_id}", response_model=result_schemas.LabResultsList)
def read_user_lab_results(
    *,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user_by_id),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve lab results for a specific user
    """
    results = db.query(models.LabResult).filter(
        models.LabResult.user_id == user.id
    ).offset(skip).limit(limit).all()
    
    total = db.query(models.LabResult).filter(
        models.LabResult.user_id == user.id
    ).count()
    
    return {"results": results, "total": total}


@router.get("/{result_id}", response_model=result_schemas.LabResult)
def read_lab_result(
    *,
    db: Session = Depends(get_db),
    result_id: int,
) -> Any:
    """
    Get a specific lab result by id
    """
    result = db.query(models.LabResult).filter(models.LabResult.id == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lab result with ID {result_id} not found",
        )
    return result


@router.put("/{result_id}", response_model=result_schemas.LabResult)
def update_lab_result(
    *,
    db: Session = Depends(get_db),
    result_id: int,
    result_in: result_schemas.LabResultUpdate,
) -> Any:
    """
    Update a lab result
    """
    result = db.query(models.LabResult).filter(models.LabResult.id == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lab result with ID {result_id} not found",
        )
    
    if result_in.test_name is not None:
        result.test_name = result_in.test_name
    
    if result_in.test_date is not None:
        result.test_date = result_in.test_date
    
    if result_in.result_value is not None:
        result.result_value = result_in.result_value
    
    if result_in.normal_range is not None:
        result.normal_range = result_in.normal_range
    
    if result_in.unit is not None:
        result.unit = result_in.unit
    
    if result_in.notes is not None:
        result.notes = result_in.notes
    
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.delete("/{result_id}", response_model=result_schemas.LabResult)
def delete_lab_result(
    *,
    db: Session = Depends(get_db),
    result_id: int,
) -> Any:
    """
    Delete a lab result
    """
    result = db.query(models.LabResult).filter(models.LabResult.id == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lab result with ID {result_id} not found",
        )
    
    db.delete(result)
    db.commit()
    return result
