from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    verify_password,
)
from app.db.database import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.services.audit import create_audit_log


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


def authenticate(
    email: str,
    password: str,
    db: Session,
):
    user = (
        db.query(User)
        .filter(User.email == email.lower())
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive",
        )

    role = db.get(Role, user.role_id)

    if not role:
        return None

    return user, role


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    authenticated = authenticate(
        data.email,
        data.password,
        db,
    )

    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    user, role = authenticated

    token = create_access_token(
        user.id,
        role.name,
    )

    create_audit_log(
        db,
        user.id,
        "LOGIN",
        "USER",
        str(user.id),
    )

    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post(
    "/login-form",
    response_model=TokenResponse,
)
def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    authenticated = authenticate(
        form_data.username,
        form_data.password,
        db,
    )

    if not authenticated:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    user, role = authenticated

    token = create_access_token(
        user.id,
        role.name,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current=Depends(get_current_user),
):
    user = current["user"]

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "role": current["role"],
        "is_active": user.is_active,
    }