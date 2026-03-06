
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, List, Optional


class BasePaginationParams(BaseModel):
    """
    Common pagination parameters for list endpoints.
    Controls page number, page size, and an option to load all items.
    """

    page: int | None = Field(
        default=1,
        gt=0,
        description="Page number starting from 1.",
        examples=[1],
    )
    pageSize: int | None = Field(
        default=10,
        gt=0,
        description="Number of items per page.",
        examples=[10],
    )
    loadAll: bool | None = Field(
        default=False,
        description="If true, ignore pagination and return all matching items.",
        examples=[False],
    )


class BaseSortParams(BaseModel):
    """
    Sorting parameters for list endpoints.
    Choose a field to sort by and direction.
    """

    sort_by: Optional[str] = Field(
        default=None,
        description="Field name to sort by (implementation-specific).",
        examples=["name"],
    )
    desc: bool = Field(
        default=False,
        description="Sort in descending order when true; ascending when false.",
        examples=[False],
    )


class BaseFilterParams(BaseModel):
    """
    Base free-text filtering parameter.
    Applies to supported searchable fields of an endpoint.
    """

    q: str | None = Field(
        default=None,
        description="Free-text search query applied to supported fields.",
        examples=["algebra"],
    )


class BaseQueryParams(BasePaginationParams, BaseSortParams):
    """
    Combined query parameters including pagination and sorting.
    Extend this with endpoint-specific filters as needed.
    """

    pass


T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    """
    Generic paginated response envelope.
    Encapsulates paging metadata and the current page of items.
    """

    page: int = Field(
        ...,
        description="Current page number (starting from 1).",
        examples=[1],
    )
    page_size: int = Field(
        ...,
        description="Configured number of items per page.",
        examples=[10],
    )
    total: int = Field(
        ...,
        description="Total number of items matching the query (across all pages).",
        examples=[123],
    )
    items: List[T] = Field(
        ...,
        description="List of items on the current page.",
    )
