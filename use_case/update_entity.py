from typing import List
from exceptions.custom_exceptions import FieldNotFoundInTemplateException, FrozenFieldCannotBeEditedException, ValidationFailedException
from models.dynamic_field import DynamicValue
from models.template import DynamicTemplate
from repository.template_repository import TemplateRepository
from repository.template_validator_repository import TemplateValidatorRepository

class UpdateEntityOf: 
    def __init__(self, template_repository: TemplateRepository, template_validator = TemplateValidatorRepository ) -> None:
        self.template_repository = template_repository
        self.template_validator = template_validator
    
    def run(self,values : List[DynamicValue], template_id: str):
        template = self.template_repository.get_template_by_id(template_id)
        
        id_field = None
        for v in values:
            if v.name == template.id_field.name:
                id_field = v
                break
            
        if not id_field:
            raise Exception("There's no way to identify the entity")
        values.remove(id_field)
            
        print("validating template")
        validator_output = self.template_validator.validate_template_update(values, template)
        
        print(validator_output)
        if validator_output:
            self.template_repository.update_entity_of(template, id_field, values)
            return True
        
        print("error, template was not validated")
        raise Exception("Cannot create entity")
 
 
        
        