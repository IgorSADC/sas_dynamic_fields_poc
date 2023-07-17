from dataclasses import dataclass
from typing import List, Tuple

from models.dynamic_field import DynamicField, DynamicFieldSignature


@dataclass
class DynamicTemplate: 
    id: str
    attributes : List[DynamicField]