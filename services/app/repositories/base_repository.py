from typing import TypeVar, Generic, Type, Optional, List
from app import db
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class

    def get_by_id(self, id: int) -> Optional[T]:
        return self.model_class.query.get(id)

    def get_all(self) -> List[T]:
        return self.model_class.query.all()

    def create(self, entity: T) -> T:
        try:
            db.session.add(entity)
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def update(self, entity: T) -> T:
        try:
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self, entity: T) -> None:
        try:
            db.session.delete(entity)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e