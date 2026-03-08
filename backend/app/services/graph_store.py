from pathlib import Path
from typing import Any

import networkx as nx
import osmnx as ox


class GraphStore:
    DATA_DIR = Path(__file__).resolve().parents[1] / "data"
    DEFAULT_FILE_NAME = "krakow.graphml"
    DEFAULT_PLACE_NAME = "Cracow, Poland"
    DEFAULT_NETWORK_TYPE = "drive"
    DEFAULT_WEIGHT = "length"
    DEFAULT_SPEED_KPH = 50.0

    CACHED_GRAPH: nx.MultiDiGraph | None = None
    CACHED_FILE_NAME: str | None = None

    @staticmethod
    def ensure_data_dir() -> Path:
        GraphStore.DATA_DIR.mkdir(parents=True, exist_ok=True)
        return GraphStore.DATA_DIR

    @staticmethod
    def normalize_graphml_name(file_name: str | None = None) -> str:
        name = file_name or GraphStore.DEFAULT_FILE_NAME
        return name if name.endswith(".graphml") else f"{name}.graphml"

    @staticmethod
    def get_graph_file_path(file_name: str | None = None) -> Path:
        GraphStore.ensure_data_dir()
        normalized_name = GraphStore.normalize_graphml_name(file_name)
        return GraphStore.DATA_DIR / normalized_name

    @staticmethod
    def download_graph_from_place(
        place_name: str,
        network_type: str = "drive",
        simplify: bool = True,
    ) -> nx.MultiDiGraph:
        return ox.graph_from_place(
            place_name,
            network_type=network_type,
            simplify=simplify,
        )

    @staticmethod
    def save_graph(graph: nx.MultiDiGraph, file_name: str | None = None) -> Path:
        graph_file_path = GraphStore.get_graph_file_path(file_name)
        ox.save_graphml(graph, filepath=str(graph_file_path))
        return graph_file_path

    @staticmethod
    def load_graph(
        file_name: str | None = None,
        place_name: str | None = None,
        network_type: str | None = None,
        simplify: bool = True,
    ) -> nx.MultiDiGraph:
        graph_file_path = GraphStore.get_graph_file_path(file_name)
        if not graph_file_path.exists():
            graph = GraphStore.download_graph_from_place(
                place_name=place_name or GraphStore.DEFAULT_PLACE_NAME,
                network_type=network_type or GraphStore.DEFAULT_NETWORK_TYPE,
                simplify=simplify,
            )
            GraphStore.save_graph(graph, file_name=file_name)
            return graph
        return ox.load_graphml(filepath=str(graph_file_path))

    @staticmethod
    def get_graph(
        file_name: str | None = None,
        place_name: str | None = None,
        network_type: str | None = None,
        simplify: bool = True,
        force_reload: bool = False,
    ) -> nx.MultiDiGraph:
        normalized_file_name = GraphStore.normalize_graphml_name(file_name)

        if (
            not force_reload
            and GraphStore.CACHED_GRAPH is not None
            and GraphStore.CACHED_FILE_NAME == normalized_file_name
        ):
            return GraphStore.CACHED_GRAPH

        graph = GraphStore.load_graph(
            file_name=normalized_file_name,
            place_name=place_name,
            network_type=network_type,
            simplify=simplify,
        )
        GraphStore.CACHED_GRAPH = graph
        GraphStore.CACHED_FILE_NAME = normalized_file_name
        return graph

    @staticmethod
    def clear_graph_cache() -> None:
        GraphStore.CACHED_GRAPH = None
        GraphStore.CACHED_FILE_NAME = None

    @staticmethod
    def to_int_if_possible(value: Any) -> Any:
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return value

    @staticmethod
    def get_nearest_node(graph: nx.MultiDiGraph, lat: float, lon: float) -> Any:
        return ox.distance.nearest_nodes(graph, X=lon, Y=lat)

    @staticmethod
    def get_k_shortest_node_paths(
        graph: nx.MultiDiGraph,
        start_node: Any,
        end_node: Any,
        k: int = 10,
        weight: str = "length",
    ) -> list[list[Any]]:
        return list(
            ox.routing.k_shortest_paths(
                graph,
                start_node,
                end_node,
                k=k,
                weight=weight,
            )
        )

    @staticmethod
    def get_path_duration_seconds(
        graph: nx.MultiDiGraph,
        node_path: list[Any],
        weight: str = "length",
    ) -> float:
        duration_s = 0.0
        for start_node, end_node in zip(node_path[:-1], node_path[1:]):
            _, edge_attr = GraphStore.choose_best_parallel_edge(
                graph=graph,
                start_node=start_node,
                end_node=end_node,
                weight=weight,
            )
            duration_s += GraphStore.estimate_travel_time_seconds(edge_attr)
        return duration_s

    @staticmethod
    def parse_speed_kph(maxspeed: Any) -> float:
        if maxspeed is None:
            return GraphStore.DEFAULT_SPEED_KPH

        if isinstance(maxspeed, list):
            for item in maxspeed:
                value = GraphStore.parse_speed_kph(item)
                if value > 0:
                    return value
            return GraphStore.DEFAULT_SPEED_KPH

        text = str(maxspeed)
        digits = "".join(ch for ch in text if ch.isdigit() or ch == ".")
        if not digits:
            return GraphStore.DEFAULT_SPEED_KPH

        value = float(digits)
        if "mph" in text.lower():
            value *= 1.60934
        return value if value > 0 else GraphStore.DEFAULT_SPEED_KPH

    @staticmethod
    def estimate_travel_time_seconds(edge_attr: dict[str, Any]) -> float:
        if edge_attr.get("travel_time") is not None:
            return float(edge_attr["travel_time"])

        length_m = float(edge_attr.get("length", 0.0))
        speed_kph = GraphStore.parse_speed_kph(edge_attr.get("maxspeed"))
        speed_m_s = max(speed_kph * 1000.0 / 3600.0, 0.1)
        return length_m / speed_m_s

    @staticmethod
    def get_edge_geometry(
        graph: nx.MultiDiGraph,
        start_node: Any,
        end_node: Any,
        edge_attr: dict[str, Any],
    ) -> list[list[float]]:
        geometry = edge_attr.get("geometry")

        if geometry is not None and hasattr(geometry, "coords"):
            return [[float(lat), float(lon)] for lon, lat in geometry.coords]

        start_data = graph.nodes[start_node]
        end_data = graph.nodes[end_node]
        return [
            [float(start_data["y"]), float(start_data["x"])],
            [float(end_data["y"]), float(end_data["x"])],
        ]

    @staticmethod
    def choose_best_parallel_edge(
        graph: nx.MultiDiGraph,
        start_node: Any,
        end_node: Any,
        weight: str,
    ) -> tuple[int, dict[str, Any]]:
        edge_data = graph.get_edge_data(start_node, end_node) or {}
        if not edge_data:
            raise ValueError(f"No edge data for pair {start_node}->{end_node}")

        best_key = None
        best_attr = None
        best_weight = float("inf")

        for edge_key, edge_attr in edge_data.items():
            candidate_weight = float(
                edge_attr.get(weight, edge_attr.get(GraphStore.DEFAULT_WEIGHT, float("inf")))
            )
            if candidate_weight < best_weight:
                best_weight = candidate_weight
                best_key = edge_key
                best_attr = edge_attr

        return int(best_key), best_attr

    @staticmethod
    def build_route_from_node_path(
        graph: nx.MultiDiGraph,
        node_path: list[Any],
        weight: str = "length",
    ) -> dict[str, Any]:
        coordinates: list[list[float]] = []
        distance_m = 0.0
        duration_s = 0.0

        for start_node, end_node in zip(node_path[:-1], node_path[1:]):
            edge_key, edge_attr = GraphStore.choose_best_parallel_edge(
                graph=graph,
                start_node=start_node,
                end_node=end_node,
                weight=weight,
            )

            length_m = float(edge_attr.get("length", 0.0))
            travel_time_s = GraphStore.estimate_travel_time_seconds(edge_attr)

            geometry = GraphStore.get_edge_geometry(
                graph=graph,
                start_node=start_node,
                end_node=end_node,
                edge_attr=edge_attr,
            )

            if not coordinates:
                coordinates.extend(geometry)
            elif geometry:
                if coordinates[-1] == geometry[0]:
                    coordinates.extend(geometry[1:])
                else:
                    coordinates.extend(geometry)

            distance_m += length_m
            duration_s += travel_time_s

        return {
            "coordinates": coordinates,
            "distance_km": round(distance_m / 1000.0, 1),
            "duration_min": int(round(duration_s / 60.0)),
        }

    @staticmethod
    def choose_personalized_path(
        graph: nx.MultiDiGraph,
        paths: list[list[Any]],
        driving_style: str | None,
        weight: str = "length",
    ) -> list[Any] | None:
        if len(paths) < 2:
            return None

        style = (driving_style or "").lower()

        if style == "dynamic":
            index = 2 if len(paths) > 2 else len(paths) - 1
            return paths[index]

        if style == "vibe":
            index = 6 if len(paths) > 6 else len(paths) - 1
            return paths[index]

        if style in {"safe", "eco"}:
            target_delta = 5 * 60.0
            fastest_duration = GraphStore.get_path_duration_seconds(
                graph=graph,
                node_path=paths[0],
                weight=weight,
            )

            best_path = None
            best_diff = float("inf")

            for path in paths[1:]:
                duration = GraphStore.get_path_duration_seconds(
                    graph=graph,
                    node_path=path,
                    weight=weight,
                )
                delta = duration - fastest_duration
                diff = abs(delta - target_delta)
                if diff < best_diff:
                    best_diff = diff
                    best_path = path

            return best_path or (paths[1] if len(paths) > 1 else None)

        return paths[1] if len(paths) > 1 else None

    @staticmethod
    def get_two_routes_between_points(
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        file_name: str | None = None,
        weight: str = "length",
        driving_style: str | None = None,
        k_paths: int = 10,
    ) -> dict[str, Any]:
        graph = GraphStore.get_graph(file_name=file_name)

        start_node = GraphStore.get_nearest_node(graph, lat=start_lat, lon=start_lon)
        end_node = GraphStore.get_nearest_node(graph, lat=end_lat, lon=end_lon)

        paths = GraphStore.get_k_shortest_node_paths(
            graph=graph,
            start_node=start_node,
            end_node=end_node,
            k=max(2, k_paths),
            weight=weight,
        )

        shortest_route = (
            GraphStore.build_route_from_node_path(
                graph=graph,
                node_path=paths[0],
                weight=weight,
            )
            if paths
            else None
        )

        personalized_path = GraphStore.choose_personalized_path(
            graph=graph,
            paths=paths,
            driving_style=driving_style,
            weight=weight,
        )

        personalized_route = (
            GraphStore.build_route_from_node_path(
                graph=graph,
                node_path=personalized_path,
                weight=weight,
            )
            if personalized_path
            else None
        )

        return {
            "driving_style": driving_style,
            "shortest_route": shortest_route,
            "personalized_route": personalized_route,
        }