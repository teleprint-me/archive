# archive/tools/db.py
from pathlib import Path
from typing import Optional, Type, Union

from peewee import Model, OperationalError, SqliteDatabase

# Create a new SqliteDatabase instance
db = SqliteDatabase("transactions.db")


class BaseModel(Model):
    """Base model class for using the database instance."""

    class Meta:
        database = db


def create_model_class(
    model_cls: Type[Model],
    label: str,
) -> Type[Model]:
    """Create a new model class that inherits from an existing model class.

    Args:
        model_cls (Type[Model]): The base model class to inherit from.
        label (str): The label to use in the name of the new class.

    Returns:
        Type[Model]: The newly created model class.
    """
    class_name = f"GL{label.capitalize()}Model"
    return type(class_name, (model_cls,), {})


def db_connect(
    model_cls: Type[Model],
    db_path: Optional[Union[str, Path]] = "",
) -> Optional[SqliteDatabase]:
    """Connect to the database and create the table if it does not exist.

    Args:
        model_cls (Type[Model]): The model class to use for creating the table. Defaults to BaseModel.
        db_path (Optional[Union[str, Path]], optional): Path to the database file. Defaults to "".

    Returns:
        Optional[SqliteDatabase]: A connected database object or None if connection fails.
    """
    db_path = db_path or Path("transactions.db")
    db = SqliteDatabase(db_path)
    model_cls._meta.database = db

    try:
        db.connect()
        if not model_cls.table_exists():
            db.create_tables([model_cls], safe=True)
        return db
    except OperationalError:
        print(f"Error connecting to {db_path}. Exiting.")
        return None
