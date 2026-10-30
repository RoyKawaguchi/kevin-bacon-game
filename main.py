import csv
import gzip
import pickle
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

GRAPH_CACHE = DATA_DIR / "actor_graph.pkl"
BACON_CACHE = DATA_DIR / "bacon_numbers.pkl"
NAMES_CACHE = DATA_DIR / "actor_names.pkl"
NAMES_FILE = DATA_DIR / "name.basics.tsv.gz"

KEVIN_BACON_ID = "nm0000102"


def load_pickle(path):
    with path.open("rb") as file:
        return pickle.load(file)


def get_actor_names(graph):
    if NAMES_CACHE.exists():
        print("Loading cached actor names...")
        return load_pickle(NAMES_CACHE)

    print("Reading IMDb names (first run only)...")
    names = {}

    with gzip.open(NAMES_FILE, "rt", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            if row["nconst"] in graph:
                names[row["nconst"]] = row["primaryName"]

    with NAMES_CACHE.open("wb") as file:
        pickle.dump(names, file, protocol=pickle.HIGHEST_PROTOCOL)

    return names


def find_actors(query, names):
    query = query.casefold()

    # Match actor ID directly
    if query in names:
        return [(query, names[query])]

    # Otherwise, search by name
    matches = [
        (actor_id, name) for actor_id, name in names.items() if query in name.casefold()
    ]

    matches.sort(
        key=lambda item: (
            item[1].casefold() != query,
            item[1].casefold(),
            item[0],
        )
    )

    return matches


def find_shortest_chain(graph, start, distances):
    """Find a shortest path from an actor to Kevin Bacon."""
    if start not in distances:
        return None

    chain = [start]
    current = start

    while current != KEVIN_BACON_ID:
        next_actors = [
            actor
            for actor in graph[current]
            if distances.get(actor) == distances[current] - 1
        ]

        if not next_actors:
            return None

        # Any neighbor with a lower Bacon number gets us closer.
        current = min(next_actors)
        chain.append(current)

    return chain


def play_game(graph, distances, names):
    print("\n=== THE KEVIN BACON GAME ===")
    print("Enter an actor's name, or type 'q' to quit.")

    while True:
        query = input("------------------------\nActor name (or IMDb ID): ").strip()

        if query.casefold() in {"q", "quit", "exit"}:
            print("Thanks for playing!")
            break

        if not query:
            continue

        matches = find_actors(query, names)

        if not matches:
            print("No matching actors found in our network.")
            continue

        if len(matches) > 1:
            print(f"\nFound {len(matches)} matches. Showing up to 10:")

            for actor_id, name in matches[:10]:
                number = distances.get(actor_id)
                result = str(number) if number is not None else "Unreachable"
                print(f"- {name} [{actor_id}] — Bacon number {result}")

            print("Try a more specific name to narrow the results.")
            continue

        actor_id, name = matches[0]
        number = distances.get(actor_id)

        print(f"\nActor: {name}")
        print(f"IMDb ID: {actor_id}")

        if number is None:
            print("Bacon number: Unreachable in our graph.")
            continue

        print(f"Bacon number: {number}")

        chain = find_shortest_chain(graph, actor_id, distances)

        if chain is None:
            print("Could not reconstruct the connection chain.")
            continue

        print("\nShortest chain:")
        print(" -> ".join(names.get(actor, actor) for actor in chain))
        print(f"\n{len(chain) - 1} connection(s) to Kevin Bacon.")


def main():
    for path in (GRAPH_CACHE, BACON_CACHE):
        if not path.exists():
            raise FileNotFoundError(
                f"Missing {path.name}. Follow the README setup steps."
            )

    print("Loading graph...")
    graph = load_pickle(GRAPH_CACHE)

    print("Loading Bacon numbers...")
    distances = load_pickle(BACON_CACHE)

    names = get_actor_names(graph)
    play_game(graph, distances, names)


if __name__ == "__main__":
    main()
