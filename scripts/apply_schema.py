from pathlib import Path
from typing import LiteralString, cast

import psycopg
from psycopg import sql

from knowledge_rag.config import settings


SQL_DIR = Path(__file__).resolve().parents[1] / "sql"


def main() -> None:
    with psycopg.connect(settings.database_url) as conn:
        for filename in (
            "001_extensions.sql",
            "002_schema.sql",
            "003_add_ai_access.sql",
        ):
            statement = (SQL_DIR / filename).read_text(encoding="utf-8")

            trusted_sql = cast(LiteralString, statement)
            conn.execute(sql.SQL(trusted_sql))

            print(f"Applied {filename}")


if __name__ == "__main__":
    main()