from pathlib import Path

import psycopg

from knowledge_rag.config import settings


SQL_DIR = Path(__file__).resolve().parents[1] / "sql"


def main() -> None:
    with psycopg.connect(settings.database_url) as conn:
        for filename in ("001_extensions.sql", "002_schema.sql"):
            sql = (SQL_DIR / filename).read_text(encoding="utf-8")
            conn.execute(sql)
            print(f"Applied {filename}")


if __name__ == "__main__":
    main()