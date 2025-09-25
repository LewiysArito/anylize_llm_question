from typing import List, Literal, Optional, Union, Any, Dict
import enum

class ColumnType:
    pass

class EngineType(enum.Enum):
    MERGETREE = "MergeTree"
    REPLACING_MERGERTREE = "ReplacingMergeTree"
    SUMMING_MERGERTREE = "SummingMergeTree"
    AGGREGATING_MERGERTREE = "AggregatingMergeTree"
    COLLAPSING_MERGERTREE = "CollapsingMergeTree"
    VERSIONED_COLLAPSING_MERGERTREE = "VersionedCollapsingMergeTree"
    GRAPHITE_MERGERTREE = "GraphiteMergeTree"
    TINY_LOG = "TinyLog"
    STRIPE_LOG = "StripeLog"
    LOG = "Log"
    MEMORY = "Memory"

class Integer(ColumnType):
    INTEGER_BITS = [8, 16, 32, 64, 128, 256]
    UNSIGNED_BITS = [8, 16, 32, 64]
    
    def __init__(self, bit: Literal[8, 16, 32, 64, 128, 256], unsigned: bool = False):
        if bit not in self.INTEGER_BITS: 
            raise ValueError(f"Integer bit value must be from the following list: {self.INTEGER_BITS}")
        
        if unsigned and bit not in self.UNSIGNED_BITS:
            raise ValueError(f"Unsigned integer bit value must be from the following list: {self.UNSIGNED_BITS}")

        self.bit = bit
        self.unsigned = unsigned

    def __str__(self):
        return f"Int{self.bit}" if not self.unsigned else f"UInt{self.bit}"
    
class String(ColumnType):
    def __init__(self, length: Optional[int] = None):
        self.length = length

    def __str__(self):
        return "String"
    
class FixedString(ColumnType):
    def __init__(self, length: int):
        self.length = length
    
    def __str__(self):
        return f"FixedString{self.length}"

class Object(ColumnType):
    def __str__(self):
        return f"JSON"

class Decimal(ColumnType):
    DECIMAL_BITS = [32, 64, 128, 256]
    def __init__(self, bit: Optional[Literal[32, 64, 128, 256]], p: Optional[int]=None, s: Optional[int]=None):
        if not bit and (not p or not s):
            raise ValueError("")
        
        if bit and bit not in self.DECIMAL_BITS:
            raise ValueError("")

        if bit and not s:
            raise ValueError("")
        
        self.bit = bit
        self.p = p
        self.s = s

    def __str__(self):
        return f"Decimal({self.p}, {self.s})" if not self.bit else f"Decimal{self.bit}({self.s})"

    
class Float(ColumnType):
    def __str__():
        return "Float32"

class Double(ColumnType):
    def __str__(self):
        return "Float64"

class BFloat16(ColumnType):
    def __str__(self):
        return "Bfloat16"
    
class DateTime(ColumnType):
    def __str__(self):
        return "DateTime"

class Date(ColumnType):
    def __str__(self):
        return "Date"
    
class Date32(ColumnType):
    def __str__(self):
        return "Date32"

class Boolean(ColumnType):
    def __str__(self):
        return "Bool"

class UUID(ColumnType):
    def __str__(self):
        return f"UUID"
    
class Time(ColumnType):
    def __str__(self):
        return "Time"
    
class Time64(ColumnType):
    def __init__(self, precision: int):
        self.precision = precision

    def __str__(self):
        return f"Time64({self.precision})"

class Enum(ColumnType):
    def __init__(self, values: List[str]):
        self.values = values
    
    def __str__(self):
        val = [f"'{v}'" for v in self.values]
        return f"Enum({', '.join(val)})"

class Array(ColumnType):
    def __init__(self, item_type: ColumnType):
        self.item_type = item_type
    
    def __str__(self):
        return f"Array({self.item_type})"
    
class Column:
    def __init__(self, name: str, type: ColumnType, 
                 primary_key: bool = False, 
                 nullable: bool = True,
                 default: Any = None):
        self.name = name
        self.type = type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
    
    def __str__(self) -> str:
        nullability = " NULL" if self.nullable else " NOT NULL"
        default = f" DEFAULT {self.default}" if self.default is not None else ""
        return f"{self.name} {self.type}{nullability}{default}"

class Table:
    def __init__(self, 
        table_name: str,
        engine: EngineType = EngineType.MERGERTREE,
        order_by: Optional[Union[str, List[str]]] = None,
        partition_by: Optional[str] = None,
        primary_key: Optional[Union[str, List[str]]] = None,
        *columns: Column
    ):
        self.table_name = table_name
        self.engine = engine
        self.order_by = order_by
        self.partition_by = partition_by
        self.primary_key = primary_key
        
        self.columns = []

        for column_obj in columns:
            if isinstance(column_obj, Column):
                self.columns.append(column_obj)

        self._columns_dict = {col.name: col for col in self.columns}

        pass

