from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from ..models.user import User
import networkx as nx

from ..dependencies import get_current_user
from ..schemas.route import RouteRequest, RouteResponse
from ..services import GraphStore

# Router: Users CRUD, authentication helpers, and profile access
route_router = APIRouter(prefix="/api/route", tags=["Routing"])


@route_router.post(
    "/",
)
async def get_route(
    payload: RouteRequest,
    current_user: Annotated[User, Depends(get_current_user)],
) -> RouteResponse:
    try:
        driving_style = (
            current_user.profile.driving_style.value
            if current_user.profile and current_user.profile.driving_style
            else None
        )

        return GraphStore.get_two_routes_between_points(
            start_lat=payload.start.lat,
            start_lon=payload.start.lon,
            end_lat=payload.end.lat,
            end_lon=payload.end.lon,
            driving_style=driving_style,
        )
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No route between provided points")
