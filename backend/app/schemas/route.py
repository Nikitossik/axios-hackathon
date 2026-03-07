from pydantic import BaseModel, Field


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
    shortest_route: RouteOut | None
    personalized_route: RouteOut | None
