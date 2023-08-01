import typing
import strawberry
import copy
import typing

import strawberry
from adapters.memory_template_repository import MemoryTemplateRepository
from adapters.validator_json_schema import ValidatorJsonSchema
from models.dynamic_field import DynamicField, DynamicFieldSignature, DynamicValue
from models.field_validators import CommonFieldValidators
from models.template import DynamicTemplate


from models.field_validators import CommonFieldValidators
from use_case.create_entity_of import CreateEntityOf
from use_case.update_entity import UpdateEntityOf


template_repo = MemoryTemplateRepository()
validator = CommonFieldValidators.no_number_validator
name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator
    )

like_pie_field = DynamicField(
        'like_pie',
        DynamicFieldSignature(frozen = False, required= False),
        None
    )

person_template = DynamicTemplate(
        'person_template',
        'PersonCollection',
        'person', 
        [name_filed],
        # id_field = name_filed
    )
json_validator = ValidatorJsonSchema()

create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)
update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)

template_repo.register_template(person_template)
print("enter")
create_entity_of_use_case.run( 
        [
            DynamicValue('name', 'Igor')
        ]
        , person_template.id
    )

print("creating schema")
import typing
import strawberry

from models.template import DynamicTemplate


def create_schema_from_dynamic_template(dynamic_template : DynamicTemplate ):
    print(dynamic_template)
    #Let's do some crazy metaprogramming thing 
    
    attributes =copy.copy(dynamic_template.attributes)
    if dynamic_template.id_field:
        attributes.append(dynamic_template.id_field)
        
    strawberry_type = strawberry.type(
        type(
        dynamic_template.entity,
        (),
        { 
         '__annotations__': {a.name : ('str' if a.signature.required else  typing.Optional[str])  for a in attributes}  # for now we just support strr
        }
            
        )
    )
    default_response = {a.name: '' for a in attributes }
    
    strawberry_query = strawberry.type(
    type(
        'Query',
        (),
        {
            f"{dynamic_template.entity}_query": strawberry.field(lambda : [strawberry_type( **{** default_response, **p}) for p in template_repo.read_entity_of(dynamic_template)]),
            '__annotations__': {
                f'{dynamic_template.entity}_query' : typing.List[strawberry_type]
            }
           
        }
        )
    )
    return strawberry_type, strawberry_query

person, query = create_schema_from_dynamic_template(person_template)
print(type(person))
print(person.__annotations__)
print(query.__annotations__)
    
print("creating schema")
schema = strawberry.Schema(query=query)
print("schema created")