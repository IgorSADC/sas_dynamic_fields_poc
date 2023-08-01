from typing import List
from exceptions.custom_exceptions import FieldNotFoundInTemplateException, MissingRequiredFieldException, ValidationFailedException
from models.dynamic_field import DynamicValue
from models.template import DynamicTemplate
from repository.template_repository import TemplateRepository
from repository.template_validator_repository import TemplateValidatorRepository
        
class CreateEntityOf: 
    def __init__(self, template_repository: TemplateRepository, template_validator = TemplateValidatorRepository ) -> None:
        self.template_repository = template_repository
        self.template_validator = template_validator
    
    def run(self,values : List[DynamicValue], template_id: str):
        template = self.template_repository.get_template_by_id(template_id)    
        validator_output = self.template_validator.validate_template_write(values, template) # Validating business rules
        
        if validator_output:
            self.template_repository.save_entity_of(template, values)
            return True
        
        raise Exception("Cannot create entity")