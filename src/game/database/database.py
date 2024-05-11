from utils.primordials import *
from typing import TypedDict, TypeVar, Callable, Union, Literal, Type, NamedTuple, Iterable

_T = TypeVar("_T")

_DatabaseSchemaType = TypeVar("_DatabaseSchemaType", covariant=NamedTuple)
_DatabaseSchemaFormat = Union[
    Literal["inmemory"],
    Literal["csv"]
]

_DatabaseProperty = TypedDict("DatabaseProperty",
    name=str, # readonly
    type=Type[_T], # readonly
    decode=Callable[[str], _T], # readonly
    encode=Callable[[_T], str] # readonly
)
_DatabaseSchema = TypedDict("DatabaseSchema",
    format=_DatabaseSchemaFormat, # readonly
    type=_DatabaseSchemaType, # readonly
    properties=list[_DatabaseProperty] # readonly
)
_Database = TypedDict("Database",
    handle=str, # readonly
    schema=_DatabaseSchema, # readonly
    entries=list[tuple]
)
DatabaseSchema = Union[_DatabaseSchema, _DatabaseSchemaType]
Database = Union[_Database, _DatabaseSchemaType]

def _database_property_new(name: str, type: Type[_T], decode: Callable[[str], _T], encode: Callable[[_T], str]) -> _DatabaseProperty:
    return dict(
        name=name,
        type=type,
        decode=decode,
        encode=encode
    )

def _database_property_get_name(property: _DatabaseProperty) -> str:
    return property["name"]

def _database_property_get_type(property: _DatabaseProperty) -> Type[_T]:
    return property["type"]

def _database_property_get_encode(property: _DatabaseProperty) -> Callable[[str], _T]:
    return property["encode"]

def _database_property_get_decode(property: _DatabaseProperty) -> Callable[[_T], str]:
    return property["decode"]

def _database_schema_new(format: _DatabaseSchemaFormat, type: Type[_DatabaseSchemaType], properties: list[_DatabaseProperty]) -> DatabaseSchema[_DatabaseSchemaType]:
    return dict(
        format=format,
        type=type,
        properties=properties
    )

def _database_schema_get_format(schema: DatabaseSchema[_DatabaseSchemaType]) -> _DatabaseSchemaFormat:
    return schema["format"]

def _database_schema_get_type(schema: DatabaseSchema[_DatabaseSchemaType]) -> _DatabaseSchemaType:
    return schema["type"]

def _database_schema_get_properties(schema: DatabaseSchema[_DatabaseSchemaType]) -> list[_DatabaseProperty]:
    return schema["properties"]

def _database_new(handle: str, schema: DatabaseSchema[_DatabaseSchemaType]) -> Database[_DatabaseSchemaType]:
    return dict(
        handle=handle,
        schema=schema,
        entries=[]
    )

def _database_load(database: Database[_DatabaseSchemaType]) -> None:
    pass

def _database_save(database: Database[_DatabaseSchemaType]) -> None:
    pass

def _database_get_handle(database: Database[_DatabaseSchemaType]) -> str:
    return database["handle"]

def _database_get_schema(database: Database[_DatabaseSchemaType]) -> DatabaseSchema[_DatabaseSchemaType]:
    return database["schema"]

def _database_get_entries(database: Database[_DatabaseSchemaType]) -> list[_DatabaseSchemaType]:
    return array_slice(database["entries"])

def _database_get_entries_length(database: Database[_DatabaseSchemaType]) -> int:
    return len(database["entries"])

def _database_get_entry_at(database: Database[_DatabaseSchemaType], i: int) -> _DatabaseSchemaType:
    return database["entries"][i]

def _database_set_entry_at(database: Database[_DatabaseSchemaType], i: int, entry: _DatabaseSchemaType) -> None:
    database["entries"][i] = entry

def _database_delete_entry_at(database: Database[_DatabaseSchemaType], i: int) -> None:
    array_splice(database["entries"], i, 1)
