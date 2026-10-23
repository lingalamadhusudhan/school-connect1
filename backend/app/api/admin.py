from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.core.security import hash_password
from app.db.database import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import CreateUserRequest
from app.services.audit import create_audit_log


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
)


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    role_name = data.role.upper()

    allowed_roles = {
        "ADMIN",
        "TEACHER",
        "PARENT",
    }

    if role_name not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail="Invalid role",
        )

    role = (
        db.query(Role)
        .filter(Role.name == role_name)
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=400,
            detail="Role does not exist",
        )

    existing = (
        db.query(User)
        .filter(User.email == data.email.lower())
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    user = User(
        full_name=data.full_name,
        email=data.email.lower(),
        phone=data.phone,
        password_hash=hash_password(data.password),
        role_id=role.id,
        is_active=True,
    )

    db.add(user)

    try:
        db.flush()

        create_audit_log(
            db,
            current["user"].id,
            "USER_CREATED",
            "USER",
            str(user.id),
            f"Created {role_name} account",
        )

        db.commit()
        db.refresh(user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email or phone already exists",
        )

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": role_name,
        "is_active": user.is_active,
    }
@router.patch("/users/{user_id}/block")
def block_user(
    user_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if user.id == current["user"].id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot block own account",
        )

    user.is_active = False

    create_audit_log(
        db,
        current["user"].id,
        "ACCOUNT_BLOCKED",
        "USER",
        str(user.id),
    )

    db.commit()

    return {
        "message": "User account blocked",
        "user_id": user.id,
    }


@router.patch("/users/{user_id}/unblock")
def unblock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current=Depends(require_admin),
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.is_active = True

    create_audit_log(
        db,
        current["user"].id,
        "ACCOUNT_UNBLOCKED",
        "USER",
        str(user.id),
    )

    db.commit()

    return {
        "message": "User account unblocked",
        "user_id": user.id,
    }