from types import FunctionType
import typing
import strawberry
import copy
import typing

import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from adapters.memory_template_repository import MemoryTemplateRepository
from adapters.validator_json_schema import ValidatorJsonSchema
from models.dynamic_field import DynamicField, DynamicFieldSignature, DynamicValue
from models.field_validators import CommonFieldValidators
from models.template import DynamicTemplate

from models.field_validators import CommonFieldValidators
from use_case.create_entity_of import CreateEntityOf
from use_case.update_entity import UpdateEntityOf


#TODO CREATE THE DYNAMIC CREATION ENDPOINT
#ADD AN ENDPOINT FOR TEMPLATE CREATION
template_repo = MemoryTemplateRepository()
validator = CommonFieldValidators.no_number_validator   
name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator
    )

last_name = DynamicField(
        'last_name',
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
        [like_pie_field,last_name],
        id_field = name_filed
    )
json_validator = ValidatorJsonSchema()

create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)
update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)

template_repo.register_template(person_template)
create_entity_of_use_case.run( 
        [
            DynamicValue('name', 'Igor'),
            DynamicValue('last_name', 'Duarte')
        ]
        , person_template.id
    )

import typing
import strawberry

from models.template import DynamicTemplate


def create_schema_from_dynamic_template(dynamic_template : DynamicTemplate ):
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
    
    def add_entity_inner(**kwargs : str): 
        create_entity_of_use_case.run([DynamicValue(v,kwargs[v]) for v in kwargs], person_template.id)
        return strawberry_type(**kwargs)
                
    from inspect import signature, Parameter
    add_entity_signature = signature(add_entity_inner)
    parameters = [Parameter(p, Parameter.KEYWORD_ONLY,annotation= strawberry_type.__annotations__[p]) for p in strawberry_type.__annotations__]
    add_entity_signature = add_entity_signature.replace(parameters=parameters,return_annotation= strawberry_type)
    
    add_entity_inner.__signature__ = add_entity_signature
    add_entity = strawberry.mutation(add_entity_inner)
    # add_entity = FunctionType(,f'add_{dynamic_template.entity}', (), {})
    
    strawberry_query = strawberry.type(
    type(
        f'Query',
        (),
        {
            f"{dynamic_template.entity}_query": strawberry.field(lambda : [strawberry_type( **{** default_response, **p}) for p in template_repo.read_entity_of(dynamic_template)]),
            '__annotations__': {
                f'{dynamic_template.entity}_query' : typing.List[strawberry_type]
            }
           
        }
        )
    )
    
    
    strawberry_mutation = strawberry.type(
        type(
            'Mutation',
            (),
            {
                f"{dynamic_template.entity}_add": add_entity,
                # '__annotations__' : {
                #     f"{dynamic_template.entity}_add": {**strawberry_type.__annotations__, 'return': strawberry_type}
                # }
                
            }
        )
    )
    
    return strawberry_type, strawberry_query, strawberry_mutation

person, query, strawberry_mutation = create_schema_from_dynamic_template(person_template)
    
schema = strawberry.Schema(query=query, mutation=strawberry_mutation)