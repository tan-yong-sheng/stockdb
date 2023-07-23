from app.loggers import setup_logging
from app.db.database_controller import create_db_and_tables

def main():
    setup_logging()
    create_db_and_tables()


if __name__ == "__main__":
    main()