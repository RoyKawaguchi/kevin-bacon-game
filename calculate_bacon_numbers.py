import pickle
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

GRAPH_CACHE = DATA_DIR / "actor_graph.pkl"
BACON_CACHE = DATA_DIR / "bacon_numbers.pkl"

KEVIN_BACON_ID = "nm0000102"


def load_pickle(path):
    with path.open("rb") as file:
        return pickle.load(file)


def calculate_bacon_numbers(graph):
    if KEVIN_BACON_ID not in graph:
        raise ValueError(
            "Kevin Bacon is missing from the graph. "
            "Check the dataset and rebuild the graph."
        )

    distances = {KEVIN_BACON_ID: 0}
    queue = deque([KEVIN_BACON_ID])

    print("Calculating shortest paths with BFS...")

    while queue:
        actor = queue.popleft()

        for costar in graph[actor]:
            if costar not in distances:
                distances[costar] = distances[actor] + 1
                queue.append(costar)

    return distances


def main():
    if not GRAPH_CACHE.exists():
        raise FileNotFoundError("Graph cache missing. Run python build_graph.py first.")

    if BACON_CACHE.exists():
        print(f"Bacon-number cache already exists: {BACON_CACHE}")
        print("Delete that file if you want to recalculate.")
        return

    graph = load_pickle(GRAPH_CACHE)
    distances = calculate_bacon_numbers(graph)

    with BACON_CACHE.open("wb") as file:
        pickle.dump(distances, file, protocol=pickle.HIGHEST_PROTOCOL)

    unreachable = len(graph) - len(distances)
    counts = Counter(distances.values())

    print(f"\nActors in graph: {len(graph):,}")
    print(f"Connected to Kevin Bacon: {len(distances):,}")
    print(f"Unreachable: {unreachable:,}")
    print("\nBacon number distribution:")

    for number in sorted(counts):
        count = counts[number]
        print(f"{number:>2}: {count:>10,} ({100 * count / len(graph):.2f}%)")

    print(f"Unreachable: {unreachable:,} ({100 * unreachable / len(graph):.2f}%)")
    print(f"\nSaved results to {BACON_CACHE}")


if __name__ == "__main__":
    main()
