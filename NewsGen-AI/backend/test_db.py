
from dotenv import load_dotenv
load_dotenv()

from app.database import (
    get_connection,
    initialize_database,
    show_database_statistics
)

try:
    print("Testing Supabase PostgreSQL connection...")

    with get_connection() as connection:
        result = connection.execute(
            "SELECT version()"
        ).fetchone()

        print("Connected successfully!")
        print("PostgreSQL:", result["version"])

    initialize_database()
    show_database_statistics()

    print("\nSUPABASE DATABASE TEST PASSED!")

except Exception as error:
    print("\nDATABASE TEST FAILED!")
    print(type(error).__name__, error)
