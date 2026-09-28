"""Download freMTPL2 raw files into data/raw/.

The project does not commit the large raw files. This downloader tries a
Hugging Face mirror first and a public GitHub mirror second.
"""
from __future__ import annotations

import sys
from pathlib import Path
import requests

from config import RAW_DIR, FREQ_PATH, SEV_PATH, FREQ_URLS, SEV_URLS


def download_one(urls: list[str], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.stat().st_size > 0:
        print(f"Already present: {destination}")
        return destination

    last_error: Exception | None = None
    for url in urls:
        try:
            print(f"Downloading {destination.name} from {url}")
            with requests.get(url, stream=True, timeout=120) as response:
                response.raise_for_status()
                with destination.open("wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            print(f"Saved {destination} ({destination.stat().st_size / 1_000_000:.1f} MB)")
            return destination
        except Exception as exc:  # noqa: BLE001 - fallback is intentional
            last_error = exc
            print(f"Source failed: {exc}")
            destination.unlink(missing_ok=True)

    raise RuntimeError(f"Could not download {destination.name}") from last_error


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    download_one(FREQ_URLS, FREQ_PATH)
    download_one(SEV_URLS, SEV_PATH)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Download failed: {exc}", file=sys.stderr)
        raise
