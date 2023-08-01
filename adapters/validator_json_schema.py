from typing import List

from jsonschema_rs import JSONSchema, validate
from models.dynamic_field import DynamicValue
from models.template import DynamicTemplate
from repository.template_validator_repository import TemplateValidatorRepository


class ValidatorJsonSchema(TemplateValidatorRepository): 
    
    def __build_write_schema_from_dynamic_template(self, dynamic_template : DynamicTemplate): 
        required_fields = []
        json_schema = { 'properties' : {}, 'type': 'object', 'additionalProperties' :False}
        
        for attribute in dynamic_template.attributes: 
            if attribute.signature.required: required_fields.append(attribute.name)
            #for writting we don't really care about frozen fields
            json_schema['properties'][attribute.name] = {'type': 'string'}
            
            if attribute.validator:
                json_schema['properties'][attribute.name][attribute.validator.validator_type] = attribute.validator.value
            
            
        if dynamic_template.id_field: 
            attribute = dynamic_template.id_field
            required_fields.append(attribute.name)
            json_schema['properties'][attribute.name] = {'type': 'string'}
            
            if attribute.validator:
                json_schema['properties'][attribute.name][attribute.validator.validator_type] = attribute.validator.value
            
        json_schema['required'] = required_fields
        print(json_schema)
        return json_schema
    
    def __build_dict_from_dynamic_value(self, values : List[DynamicValue]):
        return {d.name: d.value for d in values }
    
    
    def validate_template_write(self,json_data : List[DynamicValue], template: DynamicTemplate):
        print('BUILDING JSON SCHEMA') 
        validator  = self.__build_write_schema_from_dynamic_template(template)
        try: 
            validate(validator, self.__build_dict_from_dynamic_value( json_data))
        
            return True
        except Exception as e:
            print(e) 
            return False
    
    
    def validate_template_read(self, template : DynamicTemplate) -> bool : 
        pass 
    
    

    
    def validate_template_delete(self,template : DynamicTemplate) -> bool : 
        pass 
    
    
    def __build_update_schema_from_dynamic_template(self, dynamic_template : DynamicTemplate):
        json_schema = { 'properties' : {}, 'type': 'object', 'additionalProperties': False}
        for attribute in dynamic_template.attributes:
            #we do not add required fields to update calls
            if not attribute.signature.frozen: 
                json_schema['properties'][attribute.name] = {'type': 'string'}
                if attribute.validator:
                    json_schema['properties'][attribute.name][attribute.validator.validator_type] = attribute.validator.value
            
        return json_schema
        
    def validate_template_update(self,json_data : List[DynamicValue], template : DynamicTemplate) -> bool : 
        validator  = self.__build_update_schema_from_dynamic_template(template)
        print(self.__build_dict_from_dynamic_value( json_data))
        print(validator)
        try: 
            output = validate(validator, self.__build_dict_from_dynamic_value( json_data))
            print(f'output : {output}')
            return True
        except Exception as e:
            print(e) 
            return False
    