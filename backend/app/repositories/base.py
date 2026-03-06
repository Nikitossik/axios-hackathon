from sqlalchemy.orm import Session
from typing import Any
from ..database import Base


class BaseRepository:
    """
    Base repository providing common CRUD operations.
    Intended to be subclassed with a concrete SQLAlchemy model assigned to `model`.
    Uses a provided SQLAlchemy Session to query and persist entities.
    """

    model: Base

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.

        Args:
            db (Session): Active SQLAlchemy session used for all operations.

        Returns:
            None
        """
        self._db: Session = db

    @property
    def db(self) -> Session:
        """
        Get the underlying SQLAlchemy session.

        Returns:
            Session: The session used by this repository.
        """
        return self._db

    def query(self):
        """
        Build a query for the configured model.

        Returns:
            Query: A SQLAlchemy query object targeting `self.model`.
        """
        return self.db.query(self.model)

    def get(self, id: int | str):
        """
        Retrieve a single model instance by primary key.

        Args:
            id (int | str): Primary key value.

        Returns:
            model | None: The found instance or None if not found.
        """
        return self.query().filter(self.model.id == id).first()

    def get_multiple(self):
        """
        Retrieve all instances of the configured model.

        Returns:
            list[model]: A list of all model instances.
        """
        return self.query().all()

    def create(self, model_data: dict[str, Any]):
        """
        Create and persist a new model instance.

        Args:
            model_data (dict[str, Any]): Keyword arguments for model constructor.

        Returns:
            model: The newly created and refreshed instance.
        """
        new_instance = self.model(**model_data)
        self.db.add(new_instance)
        self.db.commit()  # Persist the new instance
        self.db.refresh(new_instance)  # Reload to get DB-generated values (e.g., id)

        return new_instance

    def update(self, db_model: Base, update_data: dict[str, Any]):
        """
        Update an existing model instance with provided data.

        Args:
            db_model (Base): The instance to update.
            update_data (dict[str, Any]): Mapping of column names to new values.

        Returns:
            Base: The updated and refreshed instance.
        """
        for column in db_model.__table__.columns:
            if column.key in update_data.keys():
                setattr(db_model, column.key, update_data[column.key])

        self.db.commit()
        self.db.refresh(db_model)
        return db_model

    def delete(self, id):
        """
        Delete a model instance by primary key.

        Args:
            id (Any): Primary key value.

        Returns:
            model | None: The deleted instance if it existed, otherwise None.
        """
        # Note: Query.get is legacy; kept for compatibility with existing code.
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj

    def delete_instance(self, instance: Base):
        """
        Delete the provided model instance.

        Args:
            instance (Base): The instance to delete.

        Returns:
            Base: The deleted instance.
        """
        self.db.delete(instance)
        self.db.commit()
        return instance