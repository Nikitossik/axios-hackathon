from typing import Generic, TypeVar, Type, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from pydantic import BaseModel
from ..schemas.shared import BaseQueryParams, PaginatedResponse

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType]):
    """
    Base service layer providing common CRUD and list operations.

    This class is intended to be subclassed per domain entity. It delegates data
    access to a repository (repo) and centralizes cross-cutting concerns such as
    pagination, sorting, filtering, and error handling.

    Attributes:
        db (Session): SQLAlchemy session used for persistence.
        model_cls (type[ModelType]): Python type representing the domain model.
        repo: Repository instance exposing query(), get(), create(), update(), delete_instance(), etc.
    """

    def __init__(self, db: Session, model_cls: Type[ModelType], repo):
        """
        Initialize the service with a database session, model class, and repository.

        Args:
            db (Session): Active SQLAlchemy session.
            model_cls (Type[ModelType]): Model class used for error messages and typing.
            repo: Repository instance responsible for data access.

        Returns:
            None
        """
        self.db = db
        self.model_cls = model_cls
        self.repo = repo

    def get_all(self) -> list[ModelType]:
        """
        Retrieve all records for the configured model.

        Returns:
            list[ModelType]: All model instances from the repository.
        """
        return self.repo.get_multiple()

    def get_paginated(
        self,
        params: BaseQueryParams,
    ) -> PaginatedResponse[ModelType]:
        """
        Retrieve a paginated list of records with optional filtering and sorting.

        The method:
        - builds a base query via repo.query()
        - applies service-level filters and sorting hooks
        - counts total items
        - applies pagination unless loadAll is true (then returns all)

        Args:
            params (BaseQueryParams): Pagination/sorting params (and extended filters in subclasses).

        Returns:
            PaginatedResponse[ModelType]: Envelope with page, page_size, total, and items.
        """
        query = self.repo.query()

        query = self.apply_filters(query, params)
        query = self.apply_sorting(query, params)

        total = query.count()

        # loadAll overrides pagination and returns the full result set
        if params.loadAll:
            params.pageSize = total if total > 0 else 1
            params.page = 1
            items = query.all()
        else:
            items = (
                query.offset((params.page - 1) * params.pageSize)
                .limit(params.pageSize)
                .all()
            )

        return PaginatedResponse(
            page=params.page,
            page_size=params.pageSize,
            total=total,
            items=items,
        )
        
    def apply_filters(self, query, params):
        """
        Hook for applying custom filters to the query.

        Override this in subclasses to add endpoint-specific filtering logic
        using values from params.

        Args:
            query: SQLAlchemy query to be filtered.
            params (BaseQueryParams): Incoming parameters carrying filter values.

        Returns:
            Any: The modified (or original) SQLAlchemy query.
        """
        return query

    def apply_sorting(self, query, params):
        """
        Apply sorting to the query if a valid sort_by field is provided.

        Args:
            query: SQLAlchemy query to be sorted.
            params (BaseQueryParams): Parameters providing sort_by and desc.

        Returns:
            Any: The query with ordering applied if possible.
        """
        if params.sort_by:
            column = getattr(self.repo.model, params.sort_by, None)
            if column is not None:
                if params.desc:
                    column = column.desc()
                query = query.order_by(column)
        return query

    def get_by_id(self, obj_id: int) -> ModelType:
        """
        Retrieve a single record by its identifier.

        Args:
            obj_id (int): Primary key of the object to retrieve.

        Returns:
            ModelType: The found instance.

        Raises:
            HTTPException: 404 if the object does not exist.
        """
        obj = self.repo.get(obj_id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model_cls.__name__} with id {obj_id} not found",
            )
        return obj

    def create(self, obj_in: Any) -> ModelType:
        """
        Create and persist a new record.

        If obj_in is a Pydantic model, it will be converted using model_dump().

        Args:
            obj_in (Any): Input data or Pydantic model for the new entity.

        Returns:
            ModelType: The newly created instance.
        """
        obj_data = obj_in

        if isinstance(obj_in, BaseModel):
            obj_data = obj_data.model_dump()

        return self.repo.create(obj_data)

    def update(self, obj_id: int, obj_in: Any) -> ModelType:
        """
        Update an existing record.

        If obj_in is a Pydantic model, it will be converted using model_dump().

        Args:
            obj_id (int): Identifier of the entity to update.
            obj_in (Any): Partial or full update payload (dict or Pydantic model).

        Returns:
            ModelType: The updated instance.

        Raises:
            HTTPException: 404 if the target object does not exist.
        """
        obj_data = obj_in

        if isinstance(obj_in, BaseModel):
            obj_data = obj_data.model_dump()

        obj = self.get_by_id(obj_id)
        return self.repo.update(obj, obj_data)

    def delete(self, obj_id: int):
        """
        Delete an existing record by its identifier.

        Args:
            obj_id (int): Identifier of the entity to delete.

        Returns:
            None

        Raises:
            HTTPException: 404 if the target object does not exist.
        """
        obj = self.get_by_id(obj_id)
        self.repo.delete_instance(obj)