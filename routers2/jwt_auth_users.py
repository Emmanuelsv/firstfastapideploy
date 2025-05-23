from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "aa9ae69daebc0ba7311c64a9c31293a5d8180b443e2109b93eb295eb297b1eea"

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


# Base de datos de ejemplo
users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2a$12$CJFwp6qNV3ezilwsTgk5e.Pv34v4aGFLjW4dOiqEZMA0ShAOSno8q"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2a$12$HHopmLLKmxOapEY51m0Ey.4.V6DEhN2xbaJos9ZWO2heQKlw.x2L6"
    }
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])  

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):    
    
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales de autenticación inválidas",
                    headers={"WWW-Authenticate": "Bearer"}
                )   
    try: 
        username = jwt.decode(token, SECRET, algorithms = [ALGORITHM]).get("sub")
        if username is None:
            raise exception
        

    except jwt.JWTError:
        raise exception

    return search_user(username) 

async def current_user(user: User = Depends(auth_user)):

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")


    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token,SECRET,algorithm=ALGORITHM), "token_type": "bearer"}

    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
