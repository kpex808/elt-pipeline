from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "cad"
DB_PATH = PROJECT_ROOT / "data" / "warehouse" / "cad" / "cad.duckdb"
TABLE = "bronze.cad_raw"


def latest_raw_file() -> Path:
    files = list(RAW_DIR.glob("cad_*.json"))
    if not files:
        raise FileNotFoundError(f"no json in {RAW_DIR}. Execute extract_cad_elt.py first.")
    return max(files, key=lambda path: path.stat().st_mtime)


def load_to_duckdb(raw_text: str, extracted_at: str) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute("CREATE SCHEMA IF NOT EXISTS bronze")
    con.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            extracted_at VARCHAR,
            payload JSON
        )
        """
    )
    con.execute(f"DELETE FROM {TABLE}")
    con.execute(
        f"INSERT INTO {TABLE} VALUES (?, ?::JSON)",
        [extracted_at, raw_text],
    )
    n = con.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
    print(f"Zeilen in {TABLE}: {n}")
    con.close()


if __name__ == "__main__":
    json_path = latest_raw_file()
    print(f"lese: {json_path.name}")
    raw_text = json_path.read_text(encoding="utf-8")
    load_to_duckdb(raw_text, json_path.stem)
    print("Fertig")
