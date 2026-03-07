from pathlib import Path

import networkx as nx
import osmnx as ox


class GraphStore:
    DATA_DIR = Path(__file__).resolve().parents[1] / "data"
    DEFAULT_FILE_NAME = "krakow.graphml"
    DEFAULT_PLACE_NAME = "Cracow, Poland"
    DEFAULT_NETWORK_TYPE = "drive"

    @staticmethod
    def ensure_data_dir() -> Path:
        GraphStore.DATA_DIR.mkdir(parents=True, exist_ok=True)
        return GraphStore.DATA_DIR

    @staticmethod
    def _normalize_graphml_name(file_name: str | None = None) -> str:
        name = file_name or GraphStore.DEFAULT_FILE_NAME
        return name if name.endswith(".graphml") else f"{name}.graphml"

    @staticmethod
    def get_graph_file_path(file_name: str | None = None) -> Path:
        GraphStore.ensure_data_dir()
        normalized_name = GraphStore._normalize_graphml_name(file_name)
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