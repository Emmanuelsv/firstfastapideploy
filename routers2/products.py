from fastapi import APIRouter

router = APIRouter(prefix= "/products",
                   tags=["products"], 
                   responses={404:{"message": "no encontrado"}})

product_list = ["Product 1", "Product 2", 
                "Product 3", "Product 4", "Product 5"]

@router.get("/")
async def products():
    return product_list


@router.get("/{id}")
async def products(id: int):
    return product_list[id]