import os

import requests
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from .JWTBearer import JWKS, JWTBearer, JWTAuthorizationCredentials
import boto3

from sqlalchemy.orm import Session
from src.crud import crud_user
from src.config.session import get_db

load_dotenv()  # Automatically load environment variables from a '.env' file.

jwks = JWKS.parse_obj(
    requests.get(
        f"https://cognito-idp.{os.environ.get('COGNITO_REGION')}.amazonaws.com/"
        f"{os.environ.get('COGNITO_POOL_ID')}/.well-known/jwks.json"
    ).json()
)

auth = JWTBearer(jwks)


async def get_current_user(credentials: JWTAuthorizationCredentials = Depends(auth), db: Session = Depends(get_db)):
    try:
        db_user = crud_user.get_user_by_email(db, email=credentials.claims["email"])
        if db_user is None:
            raise HTTPException(status_code=404, detail="Email Not found")
        return db_user.id
    except KeyError:
        HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Username missing")

def aws_session():
    return boto3.Session(aws_access_key_id= os.environ.get('ACCESS_KEY'), aws_secret_access_key=os.environ.get('ACCESS_SECRET_KEY'), region_name=os.environ.get('COGNITO_REGION'))
