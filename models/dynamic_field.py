from typing import Callable, Generic, TypeVar
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
class Validator: 
    is_valid: Callable[[str],bool ]     

@dataclass
class DynamicField:
    name : str
    signature: DynamicFieldSignature
    validator: Validator 
    