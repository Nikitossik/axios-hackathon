from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from ..models.user import User
import networkx as nx
from sqlalchemy.orm import Session

from ..dependencies import get_current_user, get_db
from ..schemas.route import (
    RouteRequest,
    RouteResponse,
    RouteChoiceRequest,
    RouteChoiceResponse,
)
from ..services import GraphStore, UserService

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

@route_router.post("/choice", response_model=RouteChoiceResponse)
async def choose_route(
    choice_request: RouteChoiceRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> RouteChoiceResponse:
    return UserService(db).apply_karma_for_route_choice(
        user=current_user,
        choice_request=choice_request,
    )
    