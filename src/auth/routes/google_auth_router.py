import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from sqlalchemy.orm import Session

from auth.constants.google_auth_constant import CALL_BACK_URI, CALL_BACK_URL, CLIENT_CONFIG, SCOPES
from auth.helper.google_userinfo_helper import get_userinfo
from auth.helper.user_helper import UserHelper
from auth.schemas.user_schema import UserInSchema, UserOutSchema
from core.dependencies.db_depend import get_session
from core.schemas.error_schema import ErrorSchema, FieldErrorSchema

google_auth_route = APIRouter(prefix='/google_auth', tags=['Google Auth'])


@google_auth_route.get('', include_in_schema=False)
def authorization_url():
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=SCOPES
    )

    flow.redirect_uri = CALL_BACK_URL

    url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return RedirectResponse(url)


@google_auth_route.get(f'/{CALL_BACK_URI}',
                       status_code=status.HTTP_201_CREATED,
                       response_model=UserOutSchema,
                       response_model_exclude_none=True,
                       responses={
                           422: {'model': FieldErrorSchema},
                           500: {'model': ErrorSchema}})
def credentials(request: Request,
                state: str = Query(),
                session: Session = Depends(get_session)):
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=None,
        state=state
    )
    flow.redirect_uri = CALL_BACK_URL

    authorization_response = str(request.url)

    # You must use https instead http. If test on localhost uncomment bellow line
    if not authorization_response.startswith('https'):
        authorization_response = authorization_response.replace('http', 'https')

    flow.fetch_token(authorization_response=authorization_response)

    google_credentials = flow.credentials
    userinfo = get_userinfo(google_credentials)

    user_in = UserInSchema(
        email=userinfo['email'],
        password=uuid.uuid4().hex,
        password_exp=datetime.now(),
        full_name=userinfo['name'],
        google_access_token=google_credentials.token,
        google_refresh_token=google_credentials.refresh_token,
    )
    user_db = UserHelper(session).create_user(user_in)

    return UserOutSchema(**user_db.__dict__)
