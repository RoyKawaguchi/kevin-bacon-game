import csv
import pickle
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"

GRAPH_CACHE = DATA_DIR / "actor_graph.pkl"
BACON_CACHE = DATA_DIR / "bacon_numbers.pkl"


def main():
    for path in (GRAPH_CACHE, BACON_CACHE):
        if not path.exists():
            raise FileNotFoundError(
                f"Missing {path.name}. Follow the README setup steps."
            )

    with GRAPH_CACHE.open("rb") as file:
        graph = pickle.load(file)

    with BACON_CACHE.open("rb") as file:
        distances = pickle.load(file)

    total = len(graph)
    counts = Counter(distances.values())
    unreachable = total - len(distances)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "bacon_distribution.csv"

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "bacon_number",
                "actor_count",
                "percentage_of_all_actors",
            ]
        )

        for number in sorted(counts):
            count = counts[number]
            writer.writerow(
                [
                    number,
                    count,
                    round(count / total * 100, 4),
                ]
            )

        writer.writerow(
            [
                "Unreachable",
                unreachable,
                round(unreachable / total * 100, 4),
            ]
        )

    print(f"Actors in graph: {total:,}")
    print(f"CSV saved to {output_path}")


if __name__ == "__main__":
    main()
