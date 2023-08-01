from dataclasses import dataclass
from typing import List, Optional, Tuple

from models.dynamic_field import DynamicField, DynamicFieldSignature


@dataclass
class DynamicTemplate: 
    id: str
    name : str
    entity  : str
    attributes : List[DynamicField]
    id_field : Optional[DynamicField] = None