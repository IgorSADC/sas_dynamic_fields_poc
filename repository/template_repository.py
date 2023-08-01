


from abc import ABCMeta, abstractmethod
from typing import List, Optional
from models.dynamic_field import DynamicField

from models.template import DynamicTemplate


class TemplateRepository(metaclass=ABCMeta):
    @abstractmethod
    def register_template(self,template: DynamicTemplate) -> bool:
        pass
    
    @abstractmethod
    def get_template_by_id(self,id : str) -> Optional[DynamicTemplate]:
         pass
     
    @abstractmethod 
    def save_entity_of(self,template: DynamicTemplate, data : List[DynamicField]):
         pass
     
    @abstractmethod
    def update_entity_of(self,template : DynamicTemplate, id_field : DynamicField, data : List[DynamicField]): 
         pass
     
    @abstractmethod
    def read_entity_of(self,template: DynamicTemplate):
         pass