import csv
import gzip
import pickle
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
GRAPH_CACHE = DATA_DIR / "actor_graph.pkl"


def load_movie_ids():
    movie_ids = set()
    path = DATA_DIR / "title.basics.tsv.gz"

    print("Reading movie titles...")

    with gzip.open(path, "rt", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            if row["titleType"] == "movie":
                movie_ids.add(row["tconst"])

    print(f"Movies found: {len(movie_ids):,}")
    return movie_ids


def build_graph(movie_ids):
    # Each movie's actor IDs.
    cast_by_movie = defaultdict(list)
    path = DATA_DIR / "title.principals.tsv.gz"

    print("Reading principal cast credits...")

    # Read the IMDb cast and crew file row by row.
    with gzip.open(path, "rt", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            # Keep only actors and actresses. Keep only movies in our movie database.
            if row["tconst"] in movie_ids and row["category"] in {"actor", "actress"}:
                cast_by_movie[row["tconst"]].append(row["nconst"])

    print(f"Movies with eligible cast: {len(cast_by_movie):,}")
    print("Building co-star connections...")

    # Store each actor and the set of their co-stars.
    graph = defaultdict(set)

    for cast in cast_by_movie.values():
        cast = list(set(cast))  # Remove duplicate actors in 1 movie

        # Select each actor in the cast.
        for i, actor in enumerate(cast):
            # Compare this actor with every actor after them.
            for costar in cast[i + 1 :]:
                graph[actor].add(costar)
                graph[costar].add(actor)

    # Convert the defaultdict into a regular dictionary.
    graph = dict(graph)

    # Count all connections and divide by two to avoid double-counting.
    edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2

    print(f"Actors with connections: {len(graph):,}")
    print(f"Unique actor connections: {edge_count:,}")

    # Return the completed actor graph.
    return graph


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if GRAPH_CACHE.exists():
        print(f"Graph cache already exists: {GRAPH_CACHE}")
        print("Delete that file if you want to rebuild the graph.")
        return

    movie_ids = load_movie_ids()
    graph = build_graph(movie_ids)

    print("Saving graph cache...")

    with GRAPH_CACHE.open("wb") as file:
        pickle.dump(graph, file, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"Saved graph to {GRAPH_CACHE}")


if __name__ == "__main__":
    main()
