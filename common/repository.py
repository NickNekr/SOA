from sqlalchemy import select

class BaseRepository:
    def __init__(self, entity, schema):
        self.entity = entity
        self.schema = schema
        
    async def get_model_by_schema(self, schema_instance, session):
        schema_attributes = schema_instance.model_dump()
        filters = []

        for field in schema_attributes:
            if hasattr(schema_instance, field):
                value = getattr(schema_instance, field)
                if not value:
                    continue
                model_attribute = getattr(self.entity, field)
                filters.append(model_attribute == value)
        
        existing_model = await session.execute(select(self.entity).where(*filters))
        existing_model = existing_model.scalar()
        return existing_model

    async def add_model_instance(self, model_instance, session):
        session.add(model_instance)
        await session.flush()
        await session.refresh(model_instance)

    async def get_by_condition(self, condition, session):
        obj = await session.execute(select(self.entity).where(condition))
        return obj.scalar()
    

    async def get_by_condition_with_exception(self, condition, session):
        obj = await session.execute(select(self.entity).where(condition))
        return obj.scalar_one()
    
    async def get_all_by_condition(self, condition, session):
        obj = await session.execute(select(self.entity).where(condition))
        obj = obj.scalars()

        if not obj:
            return []
        
        return obj.all()

    async def get_objs(self, session):
        products = await session.execute(select(self.entity))
        return list(map(lambda x: self.schema.model_validate(x), products.scalars().all()))

    async def delete_obj(self, model_instance, session):
        await session.delete(model_instance)
    
    def model_validation(self, model_instance):
        return self.schema.model_validate(model_instance)

    def create_model_by_schema(self, schema_instance):
        return self.entity(**schema_instance.model_dump())

    async def update_model(self, model_instance, updated_fields, session):
        for field, value in updated_fields.items():
            setattr(model_instance, field, value)
        await session.flush()
    
    async def update_model_by_schema(self, model_instance, schema_instance, session):
        schema_attributes = schema_instance.model_dump()

        for field, value in schema_attributes.items():
            setattr(model_instance, field, value)

        await session.flush()


# class UserRepository:
#     async def create_user(self, user: UserSchema, session: AsyncSession):
#         empty_user_data = UserData()
#         session.add(empty_user_data)
#         await session.flush()
#         await session.refresh(empty_user_data)

#         new_user = User(
#             username=user.username,
#             hashed_password=user.password,
#             user_data_id=empty_user_data.id
#         )

#         session.add(new_user)
#         await session.flush()
#         await session.refresh(new_user)

#         await session.commit()

#         return new_user.id

#     async def get_user(self, username: str, session: AsyncSession) -> User:
#         user = await session.execute(select(User).where(User.username == username))
#         return user.scalar()
