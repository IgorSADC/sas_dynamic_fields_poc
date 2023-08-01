from typing import Callable, Generic, Optional, TypeVar
from attr import dataclass


@dataclass
class DynamicValue:
    name : str
    value : str
    
@dataclass
class DynamicFieldSignature: 
    frozen: bool # not editable
    required : bool

@dataclass
class FieldValidator: 
    validator_type : str
    value : str

@dataclass
class DynamicField:
    name : str
    signature: DynamicFieldSignature
    validator: Optional[FieldValidator]
    