from pydantic import BaseModel, Field
from typing import Literal

class PointIn(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    
class RouteRequest(BaseModel):
    start: PointIn
    end: PointIn


class RouteOut(BaseModel):
    coordinates: list[list[float]]
    distance_km: float
    duration_min: int


class RouteResponse(BaseModel):
    driving_style: str | None
    shortest_route: RouteOut | None
    personalized_route: RouteOut | None

class RouteChoiceRequest(BaseModel):
    chosen_route: Literal["shortest", "personalized"]
    shortest_duration_min: int
    personalized_duration_min: int


class RouteChoiceResponse(BaseModel):
    awarded_points: int
    total_karma_points: int