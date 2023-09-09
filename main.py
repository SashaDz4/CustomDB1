from models.column import IntCol
from models.db_manager import DBManager


if __name__ == "__main__":
    # save
    db_manager = DBManager()
    db_manager.create_database("test_db")
    db_manager.add_table("test_table")
    db_manager.add_column("test_table", IntCol("amount"))
    db_manager.add_row("test_table", {"amount": 20})
    print(db_manager.get_table("test_table"))

    db_manager.add_row("test_table", {"user_type": "moderator"})
    print(db_manager.get_table("test_table"))
    db_manager.save_database("test_db1.pickle")

    # open
    db_manager = DBManager()
    db_manager.open_database("test_db1.pickle")
    print(db_manager.get_table("test_table"))
