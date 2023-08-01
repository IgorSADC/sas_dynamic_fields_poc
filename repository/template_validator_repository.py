from abc import ABCMeta, abstractmethod
from typing import List, Optional
from models.dynamic_field import DynamicValue

from models.template import DynamicTemplate


class TemplateValidatorRepository(metaclass=ABCMeta):
    
    @abstractmethod
    def validate_template_write(json_data : dict, template : DynamicTemplate) -> bool: pass
    
    @abstractmethod
    def validate_template_read(template : DynamicTemplate) -> bool : pass 

    @abstractmethod
    def validate_template_update(self,json_data : List[DynamicValue], template : DynamicTemplate) -> bool : pass
    
    @abstractmethod
    def validate_template_delete(template : DynamicTemplate) -> bool : pass 
    