import logging

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.exceptions import (
    ObjectHasDependenciesException,
    ObjectNotFoundException,
)


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filters_by, **filter_by):
        query = select(self.model).where(*filters_by).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model)
            for model in result.scalars().all()
        ]

    async def get_all(self):
        logging.info("Getting all facilities from database")
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return
        return self.schema.model_validate(model)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.schema.model_validate(model)

    async def create(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )  # type: ignore

        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def update(
        self, data: BaseModel, is_patch=False, **filter_by
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch))
        )

        result = await self.session.execute(update_stmt)

        if result.rowcount == 0:
            raise ObjectNotFoundException

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        try:
            await self.session.execute(delete_stmt)
        except IntegrityError:
            raise ObjectHasDependenciesException
