from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Database session dependency
from app.core.database import get_db

# Security & RBAC dependencies
from app.core.dependencies import get_current_user, require_admin

# Pydantic schemas
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse

# Database model
from app.models.student import Student

router = APIRouter(prefix="/students", tags=["students"])


# ==========================================
# 1. CREATE STUDENT (ADMIN ONLY)
# ==========================================
@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student (Admin only)",
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    # Check if a student with this email already exists
    existing_student = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this email already exists.",
        )

    new_student = Student(**student_data.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# ==========================================
# 2. GET ALL STUDENTS (AUTHENTICATED USERS)
# ==========================================
@router.get(
    "/",
    response_model=List[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="List all students",
)
def get_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students


# ==========================================
# 3. GET SINGLE STUDENT BY ID (AUTHENTICATED USERS)
# ==========================================
@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get student by ID",
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )
    return student


# ==========================================
# 4. UPDATE STUDENT (ADMIN ONLY)
# ==========================================
@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update student details (Admin only)",
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )

    update_dict = student_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


# ==========================================
# 5. DELETE STUDENT (ADMIN ONLY)
# ==========================================
@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student (Admin only)",
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found",
        )

    db.delete(student)
    db.commit()
    return None