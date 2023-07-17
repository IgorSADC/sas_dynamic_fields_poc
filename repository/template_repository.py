


from abc import ABCMeta, abstractmethod
from typing import Optional

from models.template import DynamicTemplate


class TemplateRepository(metaclass=ABCMeta):
    
    @abstractmethod
    def register_template(template: DynamicTemplate) -> bool:
        pass
    
    
    @abstractmethod
    def get_template_by_id(id : str) -> Optional[DynamicTemplate]:
         pass
     