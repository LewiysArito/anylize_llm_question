import re
from typing import List, Literal, Optional, Tuple, Union, Any, Dict
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
    MAX_VALUE = 256 
    def __init__(self, length: int):
        if length > self.MAX_VALUE:
            raise ValueError(f"Max byte equal {self.MAX_VALUE}")

        self.length = length
    
    def __str__(self):
        return f"FixedString({self.length})"

class Object(ColumnType):
    def __str__(self):
        return f"JSON"

class Decimal(ColumnType):
    DECIMAL_BITS = {32: 9, 64: 18, 128: 38, 256: 76}
    MAX_VALUE_P = 76
    MIN_VALUE = 0

    def __init__(self, bit: Optional[Literal[32, 64, 128, 256]] = None, 
                 p: Optional[int] = None, s: Optional[int] = None):
        
        if bit is not None and p is not None:
            raise ValueError(
                "Cannot use p when used bit. "
                "Use either Decimal(p, s)"
            )
        
        if bit is None and (p is None or s is None):
            raise ValueError(
                "For Decimal(p, s) both precision (p) and scale (s) must be specified"
            )
        if p is not None and p < self.MIN_VALUE:
            raise ValueError("Value p must be positive")
        if s is not None and s < self.MIN_VALUE:
            raise ValueError("Value s must be positive")

        if bit is not None and bit not in self.DECIMAL_BITS:
            raise ValueError(f"Bit must be from the following list: {','.join(map(str, self.DECIMAL_BITS.keys()))}")
        
        if bit is not None and s is not None and s > self.DECIMAL_BITS[bit]:
            raise ValueError(f"For Decimal{bit} scale (s) max value must be {self.DECIMAL_BITS[bit]} or less")

        if p is not None and s is not None:
            if p > self.MAX_VALUE_P:
                raise ValueError(f"Precision (p) must be {self.MAX_VALUE_P} or less")
            if s > p:
                raise ValueError(f"Scale (s) must be less or equal to precision (p)")

        self.bit = bit
        self.p = p
        self.s = s

    def __str__(self):
        if self.bit and self.s is not None:
            return f"Decimal{self.bit}({self.s})"
        elif self.p is not None and self.s is not None:
            return f"Decimal({self.p}, {self.s})"
        else:
            raise ValueError("Invalid Decimal configuration")
    
class Float(ColumnType):
    def __str__(self):
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

class IPv4(ColumnType):
    def __str__(self):
        return "IPv4"

class IPv6(ColumnType):
    def __str__(self):
        return "IPv6"

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
    def __init__(self, 
            name: str,
            type: ColumnType,
            nullable: bool = True,
            default: Optional[Any] = None):
        
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Name is cannot be empty")

        if not isinstance(type, ColumnType):
            raise ValueError("Type must be instance of ColumnType")
        
        self.name = name.strip()
        self.type = type
        self.nullable = nullable
        self.default = default

    def __str__(self) -> str:
        nullability = " NULL" if self.nullable else " NOT NULL"
        
        if isinstance(self.default, str) \
            and not re.match(r"\w+\(.*\)$", self.default)\
            and self.default.upper() != "NULL":
            default = f" DEFAULT '{self.default}'" if self.default is not None else ""
        else:
            default = f" DEFAULT {self.default}" if self.default is not None else ""

        return f"{self.name} {self.type}{nullability}{default}"

class Table:
    OPERATORS = [">", ">=", "<", "<=", "=", "IN", "IS"]
    BOOLEAN_OPERATORS = ["AND", "OR"]
    
    def __init__(self, 
        table_name: str,
        engine: EngineType = EngineType.MERGETREE,
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
        
        self.columns: List[Column] = []
        for column_obj in columns:
            if isinstance(column_obj, Column):
                self.columns.append(column_obj)

        self._columns_dict = {column_obj.name: column_obj for column_obj in self.columns}
        
        self._validate_constructor_args()
        self._validate_table_structure()
        self._validate_primary_key_order_by_relation()

    def __str__(self):
        return f"TABLE {self.table_name}"

    def _validate_constructor_args(self):
        if not self.table_name or not isinstance(self.table_name, str) or not self.table_name.strip():
            raise ValueError("Table name cannot be empty")
        
        if not isinstance(self.engine, EngineType):
            raise TypeError("Engine must be instance of EngineType")
        
        if not any([isinstance(column, Column) for column in self.columns]):
            raise ValueError("At least one Column must be provided")

    def _validate_table_structure(self):
        if self.primary_key:
            primary_keys = [self.primary_key] if isinstance(self.primary_key, str) else self.primary_key
            
            for key in primary_keys:
                if not self._columns_dict.get(key):
                    raise ValueError(f"Primary key column '{key}' not found in table columns")

                if self._columns_dict.get(key).nullable:
                    raise ValueError(f"Primary key column '{key}' cannot be nullable")

        if self.partition_by:
            search = re.search(r'\(([^)]+)\)', self.partition_by)
        
            text = search.group(1) if search else self.partition_by  
            if not any(name == text for name in [column.name for column in self.columns]):
                raise ValueError(f"Partition by column '{text}' cannot be used") 

        if self.order_by:
            order_by = [self.order_by] if isinstance(self.order_by, str) else self.order_by

            for order_col in order_by:
                if not self._columns_dict.get(order_col):
                    raise ValueError(f"Order by column '{order_col}' not found in table columns")
                
    def _validate_primary_key_order_by_relation(self):
        if not self.primary_key or not self.order_by:
            return
            
        pk_length = len(self.primary_key) if isinstance(self.primary_key, list) else 1
        order_by_length = len(self.order_by) if isinstance(self.order_by, list) else 1
        
        if pk_length > order_by_length:
            raise ValueError(
                f"PRIMARY KEY length ({pk_length}) must be less or equal ORDER BY length ({order_by_length})"
            )

    def add_column(self, column: Column):
        if column.name in self._columns_dict:
            raise ValueError(f"Column '{column.name}' already exists")
        
        self.columns.append(column)
        self._columns_dict[column.name] = column

    def generate_sql_for_create(self) -> str:
        query = f'CREATE TABLE {self.table_name}'
        query += "\n("
        for i, column in enumerate(self.columns, 1):  
            if len(self.columns) == i:
                query += f"\n\t{str(column)}"
            else:
                query += f"\n\t{str(column)},"
        query += "\n)"
        query += f"\nENGINE = {self.engine.value}"
        
        if self.partition_by:
            query += f"\nPARTITION BY {self.partition_by}"
        
        if self.primary_key:
            if isinstance(self.order_by, list): 
                query += f"\nPRIMARY KEY ({', '.join(self.primary_key)})"
            else:
                query += f"\nPRIMARY KEY {self.primary_key}"

        if isinstance(self.order_by, list): 
            query += f"\nORDER BY ({', '.join(self.order_by)})"
        else:
            query += f"\nORDER BY {self.order_by}"
        
        return query
    
    def insert(self, values: List[tuple], columns: Optional[List[str]] = None) -> str:
        if columns is None:
            columns = [column.name for column in self.columns]
        else:
            for col in columns:
                if col not in self._columns_dict:
                    raise ValueError(f"Column '{col}' not found in table '{self.table_name}'")

        if any(len(row) != len(columns) for row in values):
            raise ValueError("Each row of values must match the number of specified columns")

        columns_str = ", ".join(columns)
        values_str = ", ".join(f"({', '.join(repr(value) for value in row)})" for row in values)

        return f"INSERT INTO {self.table_name} ({columns_str}) VALUES {values_str}"
    
    def _parse_conditions(self, conditions):
        parsed_conditions = []
        for condition in conditions:
            if isinstance(condition, tuple):
                col, op, value = condition
                if col not in self._columns_dict:
                    raise ValueError(f"Column '{col}' not found in table '{self.table_name}'")
                if op not in self.OPERATORS:
                    raise ValueError(f"Invalid operator '{op}' in WHERE clause")
                parsed_conditions.append(f"{col} {op} {repr(value)}")
            elif isinstance(condition, list):
                parsed_conditions.append(f"({self.parse_conditions(condition)})")
            elif isinstance(condition, str) and condition.upper() in self.BOOLEAN_OPERATORS:
                parsed_conditions.append(condition.upper())
            else:
                raise ValueError("Invalid condition in WHERE clause")
        return " ".join(parsed_conditions)

    def select(self, columns: Optional[List[str]],
            where: Optional[List[Union[List[Union[Tuple[str, str, Any], str]], str]]] = None,
            order_by: Optional[Union[str, List[str]]] = None
        ) -> str:

        for col in columns:
            if col not in self._columns_dict:
                raise ValueError(f"Column '{col}' not found in table '{self.table_name}'")
        
        query = f"SELECT {'*' if columns is None else ', '.join(columns)} FROM {self.table}"
        
        if where:
            query += f" WHERE {self.parse_conditions(where)}"
        
        if order_by:
            if isinstance(order_by, list):
                query += f" ORDER BY {', '.join(order_by)}"
            else:
                query += f" ORDER BY {order_by}"

        return query
