# The Kevin Bacon Game

An exploration of graph theory using IMDb movie credits.

This project represents actors as nodes and connects two actors
with an undirected edge when they share a movie. Breadth-first search (BFS) calculates the shortest actor-to-actor distance from Kevin Bacon, also
known as the Bacon number.

## Features

- Interactive actor-name search
- Shortest-path Bacon numbers
- CSV export of Bacon-number statistics
- (Cached graph and results for faster repeat runs)

## Requirements

- Python 3.10 or later
- Internet connection for downloading IMDb datasets
- Sufficient disk space and RAM for processing the data (1GB of disk should be sufficient)

No third-party Python packages are required.

## Setup

Clone the repository and enter the project directory:

```bash
git clone <https://github.com/RoyKawaguchi/kevin-bacon-game>
cd kevin-bacon-game
```

Download the required IMDb datasets:

```bash
python download_data.py
```

Build the actor network:

```bash
python build_graph.py
```

Calculate Bacon numbers:

```bash
python calculate_bacon_numbers.py
```

Play the interactive interface:

```bash
python main.py
```

Export the distribution:

```bash
python export_statistics.py
```

The first build and calculation can take some time. It took about 3 minutes for me. Generated caches are saved in `data/` and reused on subsequent runs.

## Data and licensing

IMDb datasets are provided for personal, non-commercial use,
subject to IMDb's terms and licensing conditions.

Dataset documentation:
https://developer.imdb.com/non-commercial-datasets/

Dataset download location:
https://datasets.imdbws.com/

IMDb data is refreshed daily, so results may change between
runs made with different dataset versions.

Do not commit downloaded datasets or generated caches to Git.

## License

Choose a license for your own code only after checking that it
fits your intended use. A code license does not grant rights
to redistribute IMDb data.
