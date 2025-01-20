from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from api.dependencies.dependencies import AuthUOWDep, AuthServiceDep, RefreshDep, UserDep
from core.config import settings
from core.constants import REFRESH
from core.security import Security
from modules.users.responses import auth as responses
from modules.users.schemas.auth import TokenInfoSchema, LogoutResponseSchema, LoginRequestSchema

auth = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.authorization.GOOGLE_CLIENT_ID,
    client_secret=settings.authorization.GOOGLE_CLIENT_SECRET,
    server_metadata_url=settings.authorization.GOOGLE_SERVER_METADATA_URL,
    client_kwargs={"scope": "openid email profile"},
)


@auth.get("/google/login")
async def google_login(request: Request) -> Response:
    """Google authorization endpoint"""
    redirect_uri = request.url_for("callback")
    return await oauth.google.authorize_redirect(request, redirect_uri=redirect_uri)


@auth.get("/google/callback")
async def google_callback(request: Request,
                          service: AuthServiceDep,
                          uow: AuthUOWDep):
    """Google OAuth callback endpoint"""
    user = await service.google_create_user(request, oauth, uow)

    access_token = Security.create_access_token(user)
    refresh_token = Security.create_refresh_token(user)

    response = RedirectResponse(url="/")

    response.set_cookie(key=REFRESH,
                        value=refresh_token,
                        httponly=True,
                        secure=False)  # if https set True
    return response, TokenInfoSchema(access_token=access_token)


@auth.post(
           path="/login",
           summary="Login to user account (Authentication).",
           responses=responses.LOGIN_RESPONSES)
async def login(
        body: LoginRequestSchema,
        uow: AuthUOWDep,
        service: AuthServiceDep,
        response: Response,
) -> TokenInfoSchema:
    """
    Controller for logging into a user's account.
    
    Required arguments:
    * *`username`* or *`email`* *.
    
    * *`password`* - password input.
    """
    user = await service.user_authenticate(uow, body.credentials, body.password)
    access_token = Security.create_access_token(str(user.id))
    refresh_token = Security.create_refresh_token(str(user.id))

    response.set_cookie(key=REFRESH,
                        value=refresh_token, 
                        httponly=True,
                        secure=False, )  # if https set to True
    return TokenInfoSchema(access_token=access_token)


@auth.post(
    path="/refresh",
    summary="Get a new access token.",
    responses=responses.REFRESH_RESPONSES,
)
async def get_new_access_token(
    uow: AuthUOWDep,
    service: AuthServiceDep,
    refresh: RefreshDep,
) -> TokenInfoSchema:
    """
    Controller for renewing the access token.

    Arguments:
    * *`refresh_token`* - refresh token (*hidden*).
    """
    login = await service.get_user_for_update_tokens(uow, refresh)
    access_token = Security.create_access_token(login)
    return TokenInfoSchema(access_token=access_token)


@auth.post(path="/logout", summary="Logout from user account.")
async def logout_user(
    current_user: UserDep,
    response: Response,
) -> LogoutResponseSchema:
    """Controller for logging out of a user account."""
    # Later need to add a method that will log out all active sessions on this account
    response.delete_cookie(REFRESH, httponly=True, secure=True)
    return LogoutResponseSchema()
