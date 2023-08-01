import re

import pytest
from adapters.memory_template_repository import MemoryTemplateRepository
from adapters.validator_json_schema import ValidatorJsonSchema
from models.dynamic_field import DynamicField, DynamicFieldSignature, DynamicValue, FieldValidator
from models.field_validators import CommonFieldValidators
from models.template import DynamicTemplate
from use_case.create_entity_of import CreateEntityOf


class Mock:
    pass

validator = CommonFieldValidators.no_number_validator

def test_can_create_entity():    
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator

    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed],
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    create_entity_of_use_case.run(
        [
            DynamicValue(
                "name", "Igor")
        ], ""
    )

def test_cannot_create_entity_if_custom_validator_dont_pass():

    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator

    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed],
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    with pytest.raises(Exception):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "fake_name", "Igor")
            ], ""
        )
        
def test_cannot_create_entity_that_doesnt_match():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator

    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed],
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    with pytest.raises(Exception):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "0009")
            ], ""
        )
        

def test_can_skip_optional_fields():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )
    last_name_field = DynamicField(
        'last_name',
        DynamicFieldSignature(False, False),
        validator
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'person_template',
        [name_filed, last_name_field]
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    create_entity_of_use_case.run(
        [
            DynamicValue(
                "name", "Igor")
        ], ""
    )

def test_can_pass_optional_fields():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )
    last_name_field = DynamicField(
        'last_name',
        DynamicFieldSignature(False, False),
        validator
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'person_template',
        [name_filed, last_name_field]
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    create_entity_of_use_case.run(
        [
            DynamicValue(
                "name", "Igor"
            ),
            DynamicValue(
                'last_name', 'Costa'
            )
        ], ""
    )


def test_cant_pass_an_invalid_optional_fields():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )
    last_name_field = DynamicField(
        'last_name',
        DynamicFieldSignature(False, False),
        validator
    )

    person_template = DynamicTemplate(
         'person_template',
        'MainPersonTemplate',
        'person_template',
        [name_filed, last_name_field]
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    with pytest.raises(Exception):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "Igor"
                ),
                DynamicValue(
                    'last_name', '0992'
                )
            ], ""
        )


def test_cannot_pass_nonexistent_field():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )
    last_name_field = DynamicField(
        'last_name',
        DynamicFieldSignature(False, False),
        validator
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'person_template',
        [name_filed, last_name_field]
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template

    json_validator = ValidatorJsonSchema()
    create_entity_of_use_case = CreateEntityOf(template_repo, json_validator)

    with pytest.raises(Exception):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "Igor"
                ),
                DynamicValue(
                    'last_name', 'Costa'
                ),
                DynamicValue(
                    'likes_pie', 'No'
                )
            ], ""
        )
    