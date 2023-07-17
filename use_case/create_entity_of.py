from typing import List
from exceptions.custom_exceptions import FieldNotFoundInTemplateException, MissingRequiredFieldException, ValidationFailedException
from models.dynamic_field import DynamicValue
from models.template import DynamicTemplate
from repository.template_repository import TemplateRepository


class CreateEntityOf: 
    def __init__(self, template_repository: TemplateRepository ) -> None:
        self.template_repository = template_repository
    
    def run(self,values : List[DynamicValue], template_id: str):
        template = self.template_repository.get_template_by_id(template_id)
        
        values_hash = {v.name: v.value  for v in values}
        attributes_passed = 0
        for a in template.attributes:    
            was_value_passed = a.name in values_hash
            
            if was_value_passed: 
                attributes_passed +=1
                if a.validator.is_valid(values_hash[a.name]): continue
                else: 
                    raise ValidationFailedException()
            
            elif a.signature.required:
                raise MissingRequiredFieldException()
            
        if attributes_passed != len(values_hash):
            raise FieldNotFoundInTemplateException()
        return True
        
        
        
        