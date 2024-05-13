from utils.primordials import *
from utils.csv import *
from typing import TypedDict, TypeVar, Callable, Union, Literal, Type, NamedTuple

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
def _database_property_get_decode(property: _DatabaseProperty) -> Callable[[_T], str]:
    return property["decode"]
def _database_property_get_encode(property: _DatabaseProperty) -> Callable[[str], _T]:
    return property["encode"]
def _database_property_decode_value(property: _DatabaseProperty, value: str) -> _T:
    return property["decode"](value)
def _database_property_encode_value(property: _DatabaseProperty, value: _T) -> str:
    return property["encode"](value)

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
def _database_schema_decode_entry(schema: DatabaseSchema[_DatabaseSchemaType], entry: dict[str, str]) -> _DatabaseSchemaType:
    type = schema["type"]
    properties = schema["properties"]
    elements = dict()
    for property in properties:
        name = _database_property_get_name(property)
        elements[name] = _database_property_decode_value(property, entry[name])
    return type(**elements)
def _database_schema_encode_entry(schema: DatabaseSchema[_DatabaseSchemaType], entry: _DatabaseSchemaType) -> dict[str, str]:
    properties = schema["properties"]
    elements = dict()
    for property in properties:
        name = _database_property_get_name(property)
        elements[name] = _database_property_encode_value(property, getattr(entry, name))
    return elements
def _database_schema_read_handle(schema: DatabaseSchema[_DatabaseSchemaType], handle: str) -> list[_DatabaseSchemaType]:
    format = schema["format"]
    properties = schema["properties"]
    if format == "csv":
        def zipData(entry: list[str]) -> dict[str, str]:
            result = dict()
            for i in range(len(properties)):
                result[_database_property_get_name(properties[i])] = entry[i]
            return result
        return array_map(csv_read_from_file(handle), lambda e, *_: _database_schema_decode_entry(schema, zipData(e)))
    raise "Not implemented"
def _database_schema_write_handle(schema: DatabaseSchema[_DatabaseSchemaType], handle: str, entries: list[_DatabaseSchemaType]) -> None:
    format = schema["format"]
    properties = schema["properties"]
    if format == "csv":
        def unzipData(entry: dict[str, str]) -> list[str]:
            return array_map(properties, lambda p, *_: entry[_database_property_get_name(p)])
        csv_write_to_file(handle, array_map(entries, lambda e, *_: unzipData(_database_schema_encode_entry(schema, e))))
        return
    raise "Not implemented"

def _database_new(handle: str, schema: DatabaseSchema[_DatabaseSchemaType]) -> Database[_DatabaseSchemaType]:
    return dict(
        handle=handle,
        schema=schema,
        entries=[]
    )
def _database_load(database: Database[_DatabaseSchemaType]) -> None:
    handle = database["handle"]
    schema = database["schema"]
    database["entries"] = _database_schema_read_handle(schema, handle)
def _database_save(database: Database[_DatabaseSchemaType]) -> None:
    handle = database["handle"]
    schema = database["schema"]
    _database_schema_write_handle(schema, handle, database["entries"])
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
    entries = database["entries"]
    if i < len(entries):
        entries[i] = entry
    else:
        array_push(entries, entry)
def _database_delete_entry_at(database: Database[_DatabaseSchemaType], i: int) -> None:
    array_splice(database["entries"], i, 1)
