from sqlalchemy.orm import Session
import os
import botocore
from dotenv import load_dotenv
from ..config import models
from ..schema import schemas_user

from ..auth.auth import aws_session

load_dotenv()

def get_by_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas_user.User, user_id = int):
    if user.type == 'delegate':
        user.master_id = user_id
    
    db_user = models.User(
        name=user.name,
        email=user.email,
        active=user.active,
        type=user.type,
        master_id=user.master_id,
        currency = user.currency,
        country = user.country
    )

    try:
        #db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except:
        db.rollback()
        raise

    if user.type == 'delegate':
        # Create a user in Amazon Cognito
        create_cognito_user(user)

    return db_user

def get_user_by_email(db: Session, email = str):
    return db.query(models.User).filter(models.User.email == email).first()
    
def delete_user(db:Session, user_id: int):
    row_count = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return row_count

def update_user(db: Session, users: schemas_user.UserUpdate,user_id = int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    #db_user.name = users.name
    db_user.country = users.country
    db_user.currency = users.currency
    db_user.id = user_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_cognito_user(user):
    session = aws_session() 
    resource = session.client('cognito-idp')
    try:    
        response = resource.admin_create_user(
        UserPoolId = os.environ.get('COGNITO_POOL_ID'),
        Username = user.email,
        UserAttributes=[
            {
                'Name': 'name', 
                'Value': user.name
            }
        ],    
        ValidationData=[
            {
                'Name': 'name', 
                'Value': user.name
            }
        ],
        TemporaryPassword=user.password
    )
    except botocore.exceptions.ParamValidationError as e:
        raise ValueError("Invalid parameter value: %s" % e)
    except botocore.exceptions.ClientError as e:
        raise Exception("AWS service error: %s" % e)

    """
    print(response,"1111")
    response = resource.admin_initiate_auth(
        UserPoolId=os.environ.get('COGNITO_POOL_ID'),
        ClientId=os.environ.get('COGNITO_CLIENTID'),
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': user.email,
            'NEW_PASSWORD' : user.password
        }
    )
    session = response['Session']

    print(response,"2222")

    response = resource.admin_respond_to_auth_challenge(
        UserPoolId = os.environ.get('COGNITO_POOL_ID'),
        ClientId=os.environ.get('COGNITO_CLIENTID'),
        ChallengeName= 'NEW_PASSWORD_REQUIRED',
        ChallengeResponses={
            'USERNAME': user.email,
            'NEW_PASSWORD' : user.password
        },
        Session=session
    )
    print(response,"33333")
    """

    return response

def get_related_users(db: Session, id_user: int):
    id_array = []
    main = db.query(models.User.id, models.User.master_id, models.User.type).filter(models.User.id == id_user).first()
    if main:
        if main.type == 'admin':
            id_array.append(main.id)
            delegate = db.query(models.User.id, models.User.master_id, models.User.type).filter(models.User.master_id == id_user).all()
            id_array.extend([result.id for result in delegate])
        else:
            id_array = [main.id,main.master_id]
    return id_array
     
    