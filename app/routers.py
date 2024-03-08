from fastapi import APIRouter, Depends, Query
from starlette.responses import JSONResponse
from fastapi import HTTPException
from app.cruds import UserCruds, pwd_context, ItemsCruds, UserItemCrud
from app.database import db
from app.schemas import UserWithPasswordSchema, ItemSchema
from app.utils import token_auth_scheme, refresh_access_token, create_access_token, get_username_from_token

router = APIRouter()


@router.post("/api/v1/refresh-token/", tags=["Login"])
async def refresh_token(token: str = Depends(token_auth_scheme)):
    response = JSONResponse(status_code=200, content={
        "access_token": refresh_access_token(token=token)
    })
    return response


@router.post("/api/v1/user/login/", tags=["Login"])
async def user_login(user: UserWithPasswordSchema):
    user_db = await UserCruds(db=db).get_user_by_username(user.username)
    if pwd_context.verify(user.password, user_db.password):
        return {'access_token': create_access_token(user_db.username)}
    raise HTTPException(status_code=404, detail="User with this id does not exist")


@router.get("/api/v1/user/get/", tags=["User"])
async def get_by_id(id: int):
    return await UserCruds(db=db).get_user_by_id(id)


@router.get("/api/v1/user/getall/", tags=["User"])
async def get_all_user():
    return await UserCruds(db=db).get_user_all()


@router.post("/api/v1/user/register/", tags=["User"])
async def add_user(new_user: UserWithPasswordSchema):
    await UserCruds(db=db).create_user(new_user)
    return {
        "result": "user added successfully"
    }


@router.put("/api/v1/user/update/", tags=["User"])
async def update_user(new_user: UserWithPasswordSchema, username_from_jwt: str = Depends(get_username_from_token)):
    await UserCruds(db=db).update_user(new_user, username_from_jwt)
    return {
        "result": "user update successfully"
    }


@router.delete("/api/v1/user/delete/", tags=["User"])
async def delete_user(username_from_jwt: str = Depends(get_username_from_token)):
    await UserCruds(db=db).delete_user(username_from_jwt)
    return {
        "result": "user delete successfully"
    }

@router.get("/api/v1/item/get/", tags=["Item"])
async def get_by_id_item(id: int, username_from_jwt: str = Depends(get_username_from_token)):
    return await ItemsCruds(db=db).get_item_by_id(id)


@router.get("/api/v1/item/getall/", tags=["Item"])
async def get_all_item(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), username_from_jwt: str = Depends(get_username_from_token)):
    return await ItemsCruds(db=db).get_items_all(page=page, page_size=page_size)


@router.post("/api/v1/item/add/", tags=["Item"])
async def add_item(new_item: ItemSchema, username_from_jwt: str = Depends(get_username_from_token)):
    await ItemsCruds(db=db).create_item(new_item)
    return {
        "result": "item added successfully"
    }


@router.put("/api/v1/item/update/", tags=["Item"])
async def update_item(new_item: ItemSchema, id: int, username_from_jwt: str = Depends(get_username_from_token)):
    await ItemsCruds(db=db).update_item(new_item, id)
    return {
        "result": "item update successfully"
    }


@router.delete("/api/v1/item/delete/", tags=["Item"])
async def delete_item(id: int, username_from_jwt: str = Depends(get_username_from_token)):
    await ItemsCruds(db=db).delete_item(id)
    return {
        "result": "item delete successfully"
    }


@router.get("/api/v1/user-item/all/", tags=["User-item"])
async def user_all_items(username: str):
    return await UserItemCrud(db=db).get_user_items(username)


@router.post("/api/v1/user-item/add/", tags=["User-item"])
async def user_add_card(item_name: str, username_from_jwt: str = Depends(get_username_from_token)):
    await UserItemCrud(db=db).add_item_to_user(item_name, username_from_jwt)
    return {
        "result": "item added to user's inventory"
    }


@router.delete("/api/v1/user-item/delete/", tags=["User-item"])
async def user_all_items(item_name:str, username: str):
    await UserItemCrud(db=db).delete_item_from_user(item_name, username)
    return {
        "result": "item was deleted from user's inventory"
    }
