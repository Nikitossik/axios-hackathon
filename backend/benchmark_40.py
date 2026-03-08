from __future__ import annotations

import time

from app.services.graph_store import GraphStore
from app.utils.enums import UserDrivingStyleEnum


# One fixed OD pair for comparison (Kraków)
START_LAT, START_LON = 50.0617, 19.9373
END_LAT, END_LON = 50.0847, 19.9970
K_PATHS = 40
STYLES = [
	UserDrivingStyleEnum.dynamic,
	UserDrivingStyleEnum.safe,
	UserDrivingStyleEnum.eco,
	UserDrivingStyleEnum.vibe,
]


def print_top_40_candidates() -> None:
	graph = GraphStore.get_graph()

	start_node = GraphStore.get_nearest_node(graph, lat=START_LAT, lon=START_LON)
	end_node = GraphStore.get_nearest_node(graph, lat=END_LAT, lon=END_LON)

	print(f"Start node: {start_node}")
	print(f"End node: {end_node}")
	print(f"Generating top {K_PATHS} paths...\n")

	t0 = time.perf_counter()
	paths = GraphStore.get_k_shortest_node_paths(
		graph=graph,
		start_node=start_node,
		end_node=end_node,
		k=K_PATHS,
		weight="length",
	)
	t1 = time.perf_counter()

	for index, node_path in enumerate(paths, start=1):
		route = GraphStore.build_route_from_node_path(
			graph=graph,
			node_path=node_path,
			weight="length",
		)
		distance_m = int(route["distance_m"])
		duration_min = int(route["duration_min"])
		print(f"Path {index:>2}: distance_m={distance_m:>6}, duration_min={duration_min:>3}")

	total_seconds = t1 - t0
	print("\n---")
	print(f"Generated {len(paths)} paths in {total_seconds:.3f} seconds")


def print_style_comparison() -> None:
	print("\nStyle comparison with diverse k=40\n")
	print(
		f"{'style':<10} {'req_s':>8} {'short_m':>8} {'short_min':>10} "
		f"{'pers_m':>8} {'pers_min':>9} {'delta':>7} {'overlap':>8}"
	)

	graph = GraphStore.get_graph()
	start_node = GraphStore.get_nearest_node(graph, lat=START_LAT, lon=START_LON)
	end_node = GraphStore.get_nearest_node(graph, lat=END_LAT, lon=END_LON)

	for style in STYLES:
		style_name = style.value

		t0 = time.perf_counter()
		paths = GraphStore.get_diverse_node_paths(
			graph=graph,
			start_node=start_node,
			end_node=end_node,
			n=K_PATHS,
			base_weight="length",
		)

		shortest_path = paths[0] if paths else None
		personalized_path = GraphStore.choose_personalized_path(
			graph=graph,
			paths=paths,
			driving_style=style_name,
			weight="length",
		)

		shortest_route = (
			GraphStore.build_route_from_node_path(graph=graph, node_path=shortest_path, weight="length")
			if shortest_path
			else {}
		)
		personalized_route = (
			GraphStore.build_route_from_node_path(graph=graph, node_path=personalized_path, weight="length")
			if personalized_path
			else {}
		)
		t1 = time.perf_counter()

		short_m = int(shortest_route.get("distance_m", 0))
		short_min = int(shortest_route.get("duration_min", 0))
		pers_m = int(personalized_route.get("distance_m", 0))
		pers_min = int(personalized_route.get("duration_min", 0))
		delta_min = max(0, pers_min - short_min)

		overlap = (
			GraphStore.path_overlap_ratio(shortest_path, personalized_path)
			if shortest_path and personalized_path
			else 1.0
		)

		print(
			f"{style_name:<10} {t1 - t0:>8.3f} {short_m:>8} {short_min:>10} "
			f"{pers_m:>8} {pers_min:>9} {delta_min:>7} {overlap:>8.3f}"
		)


def main() -> None:
	GraphStore.get_graph()
	print_top_40_candidates()
	print_style_comparison()


if __name__ == "__main__":
    main()
