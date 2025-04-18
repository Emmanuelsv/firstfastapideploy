from fastapi import FastAPI
from routers2 import products, users , basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI() 

#Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


app.mount("/static",StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "¡Hola FastAPI!"

# url local : http://127.0.0.1:8000

@app.get("/url")
async def url():
    return { "url" : "https://mouredev.com" }
