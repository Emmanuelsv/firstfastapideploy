from fastapi import APIRouter,HTTPException

from pydantic import BaseModel


router = APIRouter(prefix ="/users",
                   tags = ["users"],
                   responses ={404:{"message": "no encontrado"}})

# Iniciar el server: uvicorn users:app --reload


#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Emmanuel", surname="Sanchez", url="https://emmanueldev.com", age=25),
              User(id=2, name="Sanchez", surname="Dev", url="https://mouredev.com", age=33),
              User(id=3, name="Alejandro", surname="Desarrollador", url="https://Alejandro.com", age=28)]


@router.get("/usersjson")
async def usersjson():
    return [{"name": "Emmanuel", "surname" : "Sanchez", "url" : "https://emmanueldev.com", "age" : 25},
            {"name": "Sanchez", "surname" : "Dev", "url" : "https://mouredev.com", "age" : 33},
            {"name": "Alej  andro", "surname" : "Desarrollador", "url" : "https://Alejandro.com", "age" : 28} ]


@router.get("/")
async def users():
    return users_list

#Path
@router.get("/{id}", response_model=User, status_code=200)
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    user = next(users, None)  # Obtiene el primer usuario o None si está vacío
    if user is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado el usuario")
    return user


@router.get("/")  # Query
async def user(id: int):
    return search_user(id)

@router.post("/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) ==User:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
        
    users_list.append(user)
    return user

@router.put("/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id ==user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error" : "No se ha actulizado el usuario" }
    else:
        return user

@router.delete("/{id}")
async def user(id: int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True 
            break
        
    if not found:
        return {"error" : "No se ha eliminado el usuario" }

    
def search_user(id: int):

    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    
    except:
        return {"error" : "No se ha encontrado el usuario" }
    

