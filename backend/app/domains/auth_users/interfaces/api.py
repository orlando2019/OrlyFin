from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status

from app.core.config import settings
from app.core.errors import AppError
from app.core.rate_limit import limit_requests
from app.core.security import jwt_cookie_policy
from app.domains.auth_users.application.schemas import AuthUserResponse, LoginRequest, UserCreateRequest
from app.domains.auth_users.application.service import AuthUsersService, get_auth_users_service, get_current_user
from app.domains.auth_users.infrastructure.models import User
from app.domains.rbac.application.service import RbacService
from app.domains.rbac.interfaces.dependencies import require_permission
from app.domains.auth_users.interfaces.schemas import AuthMessageResponse, MeResponse

router = APIRouter(prefix="/auth", tags=["auth"])
users_router = APIRouter(prefix="/users", tags=["users"])


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    cookie_domain = None if jwt_cookie_policy.domain in {"", "localhost"} else jwt_cookie_policy.domain
    response.set_cookie(
        key=settings.jwt_access_cookie_name,
        value=access_token,
        httponly=True,
        secure=jwt_cookie_policy.secure,
        samesite=jwt_cookie_policy.samesite,
        domain=cookie_domain,
        max_age=jwt_cookie_policy.access_token_minutes * 60,
        path="/",
    )
    response.set_cookie(
        key=settings.jwt_refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=jwt_cookie_policy.secure,
        samesite=jwt_cookie_policy.samesite,
        domain=cookie_domain,
        max_age=jwt_cookie_policy.refresh_token_days * 24 * 60 * 60,
        path="/",
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(settings.jwt_access_cookie_name, path="/")
    response.delete_cookie(settings.jwt_refresh_cookie_name, path="/")


@router.post("/login", response_model=AuthUserResponse)
def login(
    payload: LoginRequest,
    response: Response,
    _: None = limit_requests("auth_login", limit=8, window_seconds=60),
    auth_service: AuthUsersService = Depends(get_auth_users_service),
) -> AuthUserResponse:
    user, auth_info = auth_service.authenticate(payload.email, payload.password)
    access_token, refresh_token = auth_service.issue_token_pair(user, auth_info["claims"])
    _set_auth_cookies(response, access_token, refresh_token)

    return AuthUserResponse(
        id=user.id,
        organization_id=user.organization_id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        roles=auth_info["roles"],
        permissions=auth_info["permissions"],
    )


@router.post("/refresh", response_model=AuthMessageResponse)
def refresh_token(
    request: Request,
    response: Response,
    auth_service: AuthUsersService = Depends(get_auth_users_service),
) -> AuthMessageResponse:
    refresh_token = request.cookies.get(settings.jwt_refresh_cookie_name)
    if not refresh_token:
        raise AppError("UNAUTHORIZED", "Refresh token missing", 401)

    user = auth_service.decode_and_get_user(refresh_token, token_type="refresh")
    roles = auth_service.rbac_service.get_user_roles(user.id)
    claims = {"org": user.organization_id, "roles": roles}
    new_access, new_refresh = auth_service.issue_token_pair(user, claims)
    _set_auth_cookies(response, new_access, new_refresh)
    return AuthMessageResponse(message="Tokens refreshed")


@router.post("/logout", response_model=AuthMessageResponse)
def logout(response: Response) -> AuthMessageResponse:
    _clear_auth_cookies(response)
    return AuthMessageResponse(message="Session closed")


@router.get("/me", response_model=MeResponse)
def me(
    current_user: User = Depends(get_current_user),
    auth_service: AuthUsersService = Depends(get_auth_users_service),
) -> MeResponse:
    roles = auth_service.rbac_service.get_user_roles(current_user.id)
    permissions = auth_service.rbac_service.get_user_permission_keys(current_user.id)
    return MeResponse(
        id=current_user.id,
        organization_id=current_user.organization_id,
        email=current_user.email,
        full_name=current_user.full_name,
        roles=roles,
        permissions=permissions,
    )


@users_router.post(
    "",
    response_model=MeResponse,
    dependencies=[Depends(require_permission("auth_users", "create"))],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    payload: UserCreateRequest,
    auth_service: AuthUsersService = Depends(get_auth_users_service),
    current_user: User = Depends(get_current_user),
) -> MeResponse:
    user = auth_service.create_user(
        organization_id=current_user.organization_id,
        email=payload.email,
        full_name=payload.full_name,
        password=payload.password,
        role_names=payload.role_names,
    )
    rbac = RbacService(auth_service.db)
    return MeResponse(
        id=user.id,
        organization_id=user.organization_id,
        email=user.email,
        full_name=user.full_name,
        roles=rbac.get_user_roles(user.id),
        permissions=rbac.get_user_permission_keys(user.id),
    )
