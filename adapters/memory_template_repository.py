from typing import List, Optional
from jsonschema_rs import JSONSchema, validate

from models.dynamic_field import DynamicField, DynamicValue
from models.template import DynamicTemplate
from repository.template_repository import TemplateRepository

DynamicObject = dict

class MemoryTemplateRepository(TemplateRepository):
    
    def __init__(self): 
        self.templates = {}
        self.entities = {}
        
    def register_template(self, template: DynamicTemplate) -> bool:
        self.templates[template.id] = template
        
    def get_template_by_id(self, template_id : str) -> Optional[DynamicTemplate]:
        if template_id in self.templates:
            return self.templates[template_id]
        return None
    
    def save_entity_of(self, template: DynamicTemplate, data : List[DynamicValue]):
         if template.name not in self.entities: 
             self.entities[template.name] = []
         self.entities[template.name].append({d.name: d.value for d in data})
         
         
    def update_entity_of(self, template: DynamicTemplate, id_field : DynamicValue, data: List[DynamicValue]):
        entity = self.__get_entity_by_id(template, id_field)
        self.entities[template.name].remove(entity)
        entity = {** entity, **{d.name:d.value for d in data}}
        self.entities[template.name].append(entity)
        
        
    def __get_entity_by_id(self,template: DynamicTemplate, id_field: DynamicValue) -> DynamicObject:
         for entitiy in self.entities[template.name]:
            if entitiy[id_field.name] == id_field.value:
                return entitiy
             
             
    def __build_read_schema(self, dynamic_template: DynamicTemplate):
        required_fields = []
        json_schema = { 'properties' : {}, 'type': 'object', 'additionalProperties' :True} #We should allow additional properties for reading
        
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
        return json_schema
        
    def __filter_entity_by_template(self, template : DynamicTemplate, entity : dict):
        # this function should remove any additional non authorized fields from the entity 
        fields = [f.name for f in template.attributes]
        if template.id_field:
            fields.append(template.id_field.name)
        
        return {f: entity[f] for f in entity if f in fields}
    def read_entity_of(self, template: DynamicTemplate):
        matches = []
        schema = self.__build_read_schema(template)
        print(schema)
        
        for entity in self.entities[template.name]:
            try: 
                print(entity)
                validate(schema, entity)
                matches.append(self.__filter_entity_by_template(template, entity))
            except Exception as e:
                print(e)
                continue
                
        return matches