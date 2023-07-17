from typing import List
from exceptions.cusotm_exceptions import FieldNotFoundInTemplateException, FrozenFieldCannotBeEditedException, ValidationFailedException
from models.dynamic_field import DynamicValue
from models.template import DynamicTemplate


def can_edit_entity(template : DynamicTemplate, values : List[DynamicValue] ):   
    template_hash = {a.name: a for a in template.attributes}
    
    for value in values: 
        if value.name not in template_hash:
            raise FieldNotFoundInTemplateException()
    
        if template_hash[value.name].signature.frozen: 
            raise FrozenFieldCannotBeEditedException()
        
        
        if not template_hash[value.name].validator.is_valid(value.value):
            raise ValidationFailedException()
        
    return True
 
 
        
        