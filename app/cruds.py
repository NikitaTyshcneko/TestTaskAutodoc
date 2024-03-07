import databases
from passlib.context import CryptContext
from fastapi import HTTPException, Query
from app.models import users, items, user_item
from app.query_utils import is_user_has_this_item, user_item_tuple, get_user
from app.schemas import UserSchema, UserWithPasswordSchema, ItemSchema

# This is used to hash passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_by_id(self, id: int):
        user = await self.db.fetch_one(users.select().where(users.c.id == id))
        if user == None:
            raise HTTPException(status_code=404, detail="User with this id does not exist")
        return UserSchema(id=user.id, username=user.username, password=user.password)

    async def get_user_by_username(self, username: str):
        user = await get_user(self.db, username)
        return UserWithPasswordSchema(id=user.id, username=user.username, password=user.password)

    async def get_user_all(self):
        user_db = await self.db.fetch_all(users.select())
        if user_db == None:
            return None
        return [UserSchema(id=user.id, username=user.username, password=user.password) for
                user in user_db]

    async def create_user(self, new_user: UserWithPasswordSchema):
        user = await self.db.fetch_one(users.select().where(users.c.username == new_user.username))
        if user != None:
            raise HTTPException(status_code=404, detail="User with this username already exists")
        hashed_password = pwd_context.hash(new_user.password)
        query = users.insert().values(username=new_user.username, password=hashed_password)
        await self.db.execute(query)
        return "success"

    async def update_user(self, new_user: UserWithPasswordSchema, username: str):
        query = users.update().values(username=new_user.username, password=pwd_context.hash(new_user.password)).where(
            users.c.username == username)
        await self.db.execute(query)
        return "success"

    async def delete_user(self, username: str):
        query = users.delete().where(users.c.username == username)
        await self.db.execute(query)
        return "success"


class ItemsCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_item_by_id(self, id: int):
        item = await self.db.fetch_one(items.select().where(items.c.id == id))
        if item is None:
            raise HTTPException(status_code=404, detail="Item with this id does not exist")
        return ItemSchema(id=item.id, name=item.name, description=item.description, category=item.category,
                          quantity=item.quantity, price=item.price)

    async def get_items_all(self, page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
        offset = (page - 1) * page_size

        items_db = await self.db.fetch_all(items.select().offset(offset).limit(page_size))
        if items_db is None:
            return None
        return [ItemSchema(id=item.id, name=item.name, description=item.description, category=item.category,
                           quantity=item.quantity, price=item.price) for item in items_db]

    async def create_item(self, new_item: ItemSchema):
        query = items.insert().values(name=new_item.name, description=new_item.description, category=new_item.category,
                                      quantity=new_item.quantity, price=new_item.price)
        await self.db.execute(query)
        return "success"

    async def update_item(self, new_item: ItemSchema, id: int):
        query = items.update().values(name=new_item.name, description=new_item.description, category=new_item.category,
                                      quantity=new_item.quantity, price=new_item.price).where(items.c.id == id)
        await self.db.execute(query)
        return "success"

    async def delete_item(self, id: int):
        query = items.delete().where(items.c.id == id)
        await self.db.execute(query)
        return "success"


class UserItemCrud:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_items(self, username: str):
        user = await get_user(self.db, username)

        user_item_db = await self.db.fetch_all(user_item.select().where(user_item.c.user_id == user.id))

        if user_item_db is None:
            raise HTTPException(status_code=404, detail="user_item_db not found")

        item_ids = [user_in_db.item_id for user_in_db in user_item_db]

        items_db = await self.db.fetch_all(items.select().where(items.c.id.in_(item_ids)))

        return [ItemSchema(id=item.id, name=item.name, description=item.description, category=item.category,
                           quantity=item.quantity, price=item.price) for item in items_db]

    async def add_item_to_user(self, item_name: str, username_from_jwt):
        user_and_item = await user_item_tuple(self.db, item_name, username_from_jwt)
        user_item_association = await is_user_has_this_item(self.db, *user_and_item)

        user = user_and_item[0]
        item = user_and_item[1]

        if user_item_association:
            raise HTTPException(status_code=404, detail="User already has this item")

        query = user_item.insert().values(user_id=user.id, item_id=item.id)
        await self.db.execute(query)
        return "success"

    async def delete_item_from_user(self, item_name: str, username_from_jwt: str):
        user_and_item = await user_item_tuple(self.db, item_name, username_from_jwt)
        user_item_association = await is_user_has_this_item(self.db, *user_and_item)

        user = user_and_item[0]
        item = user_and_item[1]

        if user_item_association is None:
            raise HTTPException(status_code=404, detail="User does not have this item")

        query = user_item.delete().where(
            (user_item.c.user_id == user.id) & (user_item.c.item_id == item.id)
        )
        await self.db.execute(query)
        return "success"
