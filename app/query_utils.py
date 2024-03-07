from fastapi import HTTPException
from app.models import user_item, users, items


async def get_user(db, username:str):
    user = await db.fetch_one(users.select().where(users.c.username == username))
    if user is None:
        raise HTTPException(status_code=404, detail="User with this username does not exist")
    return user

async def is_user_has_this_item(db, user, item):
    return await db.fetch_one(
            user_item.select().where((user_item.c.user_id == user.id) & (user_item.c.item_id == item.id)))


async def user_item_tuple(db, item_name: str, username_from_jwt: str):
    user = await db.fetch_one(users.select().where(users.c.username == username_from_jwt))
    item = await db.fetch_one(items.select().where(items.c.name == item_name))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if item is None:
        raise HTTPException(status_code=404, detail="Item was not found")

    return (user, item)

