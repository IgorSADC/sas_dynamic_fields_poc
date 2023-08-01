import pytest
from adapters.memory_template_repository import MemoryTemplateRepository
from adapters.validator_json_schema import ValidatorJsonSchema
from models.dynamic_field import DynamicField, DynamicFieldSignature, DynamicValue
from models.field_validators import CommonFieldValidators
from models.template import DynamicTemplate
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
        'Person', 
        [like_pie_field],
        id_field = name_filed
    )
json_validator = ValidatorJsonSchema()

create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)
update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)


def test_can_register_template():
    template_repo.register_template(person_template) 
    
def test_can_create_entity_of_template():
    create_entity_of_use_case.run( 
        [
            DynamicValue('name', 'Igor')
        ]
        , 'person_template'   
    )

def test_can_query_entity_of(): 
    entities  = template_repo.read_entity_of(person_template) # {name : ''}
    assert len(entities) == 1
    assert entities[0]['name'] == 'Igor'  
    
    with pytest.raises(Exception): 
        entities[0]['likes_pie']
    
def test_can_update_entity_of(): 
    update_entity_of_use_case.run(
        [
            DynamicValue('name', 'Igor'),
            DynamicValue('like_pie', 'Yes, he sure does!')
        ],
        person_template.id
    )
    
def test_the_value_really_updated(): 
    print(template_repo.entities)
    entities  = template_repo.read_entity_of(person_template)
    assert len(entities) == 1
    assert entities[0]['name'] == 'Igor' 
    assert entities[0]['like_pie'] == 'Yes, he sure does!'
    
    
def test_can_query_only_templated_fields():
    pielover_template = DynamicTemplate('pielover',
        'PersonCollection',
        'PieS3',
        [ like_pie_field],
    )
    
    entities = template_repo.read_entity_of(pielover_template)
    assert len(entities) == 1
    assert entities[0]['like_pie'] == 'Yes, he sure does!'
    with pytest.raises(Exception):
        entities[0]['name']
     