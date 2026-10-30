from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

FILES = [
    "name.basics.tsv.gz",  # People
    "title.basics.tsv.gz",  # Movies/Shows
    "title.principals.tsv.gz",  # Cast + Key crew
]

BASE_URL = "https://datasets.imdbws.com/"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        destination = DATA_DIR / filename

        if destination.exists() and destination.stat().st_size > 0:
            print(f"Already downloaded: {filename}")
            continue

        url = BASE_URL + filename
        print(f"Downloading {filename} ...")

        try:
            urlretrieve(url, destination)
            print(f"Saved: {destination}")
        except Exception:
            destination.unlink(missing_ok=True)
            raise

    print("\nAll required IMDb datasets are ready.")


if __name__ == "__main__":
    main()
