from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"

FREQ_PATH = RAW_DIR / "freMTPL2freq.csv"
SEV_PATH = RAW_DIR / "freMTPL2sev.csv"

FREQ_URLS = [
    "https://huggingface.co/datasets/mabilton/fremtpl2/resolve/main/freMTPL2freq.csv?download=true",
    "https://raw.githubusercontent.com/PNM0792/auto-insurance-pricing/main/automobile/data/freMTPL2freq.csv",
]
SEV_URLS = [
    "https://huggingface.co/datasets/mabilton/fremtpl2/resolve/main/freMTPL2sev.csv?download=true",
    "https://raw.githubusercontent.com/PNM0792/auto-insurance-pricing/main/automobile/data/freMTPL2sev.csv",
]

RANDOM_STATE = 42
TEST_SIZE = 0.20
