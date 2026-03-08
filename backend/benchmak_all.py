from __future__ import annotations

import statistics
import time
from typing import Any

from app.services.graph_store import GraphStore
from app.utils.enums import UserDrivingStyleEnum


# Пары точек в Кракове (lat, lon)
OD_PAIRS = [
    ((50.0617, 19.9373), (50.0847, 19.9970)),  # центр -> северо-восток
    ((50.0497, 19.9449), (50.0758, 19.8615)),  # юг-центр -> запад
]

K_VALUES = [10, 20, 30, 40]
STYLES = [
    UserDrivingStyleEnum.dynamic,
    UserDrivingStyleEnum.safe,
    UserDrivingStyleEnum.eco,
    UserDrivingStyleEnum.vibe,
]
REPEATS = 2  # повторов на одну комбинацию


def run_once(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    style: Any,
    k_paths: int,
) -> dict[str, Any]:
    return GraphStore.get_two_routes_between_points(
        start_lat=start_lat,
        start_lon=start_lon,
        end_lat=end_lat,
        end_lon=end_lon,
        driving_style=style,
        k_paths=k_paths,
    )


def benchmark() -> None:
    # warmup: граф в кэш (важно, чтобы не мерить чтение с диска)
    GraphStore.get_graph()

    print("Benchmark started...\n")
    print(
        f"{'style':<10} {'k':<4} {'avg_s':>8} {'min_s':>8} {'max_s':>8} "
        f"{'short_km':>9} {'short_min':>10} {'pers_km':>9} {'pers_min':>9} {'delta_min':>10}"
    )

    for style in STYLES:
        style_name = style.value if hasattr(style, "value") else str(style)

        for k in K_VALUES:
            timings_s: list[float] = []
            deltas_min: list[float] = []
            shortest_dist_km: list[float] = []
            shortest_dur_min: list[float] = []
            personalized_dist_km: list[float] = []
            personalized_dur_min: list[float] = []

            for _ in range(REPEATS):
                for (start, end) in OD_PAIRS:
                    t0 = time.perf_counter()
                    result = run_once(
                        start_lat=start[0],
                        start_lon=start[1],
                        end_lat=end[0],
                        end_lon=end[1],
                        style=style,
                        k_paths=k,
                    )
                    t1 = time.perf_counter()
                    timings_s.append(t1 - t0)

                    shortest = result.get("shortest_route") or {}
                    personalized = result.get("personalized_route") or {}

                    s_dist = float(shortest.get("distance_km", 0))
                    s_min = float(shortest.get("duration_min", 0))

                    p_dist = float(personalized.get("distance_km", 0))
                    p_min = float(personalized.get("duration_min", 0))

                    shortest_dist_km.append(s_dist)
                    shortest_dur_min.append(s_min)
                    personalized_dist_km.append(p_dist)
                    personalized_dur_min.append(p_min)
                    deltas_min.append(max(0.0, p_min - s_min))

            avg_s = statistics.mean(timings_s) if timings_s else 0.0
            min_s = min(timings_s) if timings_s else 0.0
            max_s = max(timings_s) if timings_s else 0.0

            avg_short_km = statistics.mean(shortest_dist_km) if shortest_dist_km else 0.0
            avg_short_min = statistics.mean(shortest_dur_min) if shortest_dur_min else 0.0
            avg_pers_km = statistics.mean(personalized_dist_km) if personalized_dist_km else 0.0
            avg_pers_min = statistics.mean(personalized_dur_min) if personalized_dur_min else 0.0
            avg_delta = statistics.mean(deltas_min) if deltas_min else 0.0

            print(
                f"{style_name:<10} {k:<4} {avg_s:>8.3f} {min_s:>8.3f} {max_s:>8.3f} "
                f"{avg_short_km:>9.1f} {avg_short_min:>10.1f} {avg_pers_km:>9.1f} {avg_pers_min:>9.1f} {avg_delta:>10.1f}"
            )

    print("\nDone.")


if __name__ == "__main__":
    benchmark()