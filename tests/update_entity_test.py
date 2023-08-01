
import pytest
from adapters.memory_template_repository import MemoryTemplateRepository
from adapters.validator_json_schema import ValidatorJsonSchema
from models.dynamic_field import DynamicField, DynamicFieldSignature, DynamicValue
from models.field_validators import CommonFieldValidators
from models.template import DynamicTemplate
from use_case.update_entity import UpdateEntityOf

class Mock:
    pass

validator = CommonFieldValidators.no_number_validator
def test_can_update_entity():    
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator
    )
    
    like_pie_field = DynamicField(
        'like_pie',
        DynamicFieldSignature(frozen= False, required= False),
        None
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed, like_pie_field],
        id_field= name_filed
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template
    template_repo.update_entity_of = lambda *args, **kwargs: True

    json_validator = ValidatorJsonSchema()
    update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)

    update_entity_of_use_case.run(
        [
            DynamicValue(
                'name', 'Igor'),
            DynamicValue(
                "like_pie", "Yes")
        ], ""
    )


def test_cannot_update_frozen_field():    
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=True),
        validator
    )
    
    like_pie_field = DynamicField(
        'like_pie',
        DynamicFieldSignature(frozen= True, required= False),
        None
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed, like_pie_field],
        id_field= name_filed
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template
    template_repo.update_entity_of = lambda *args, **kwargs: True

    json_validator = ValidatorJsonSchema()
    update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)


    with pytest.raises(Exception):
        update_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "Igor"),
                DynamicField('like_pie', 'NONON')
            ], ""
        )


def test_can_update_one_field_without_updating_another():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=False),
        validator
    )
    
    like_pie_field = DynamicField(
        'like_pie',
        DynamicFieldSignature(frozen= False, required= False),
        None
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed, like_pie_field],
        id_field= name_filed
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template
    template_repo.update_entity_of = lambda *args, **kwargs: True

    json_validator = ValidatorJsonSchema()
    update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)


    update_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "Costa")
            ], ""
        )


def test_cannot_update_field_if_it_doesnt_match_validator():
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(required= True, frozen=False),
        validator
    )
    
    like_pie_field = DynamicField(
        'like_pie',
        DynamicFieldSignature(frozen= False, required= False),
        validator
    )

    person_template = DynamicTemplate(
        'person_template',
        'MainPersonTemplate',
        'Person', 
        [name_filed, like_pie_field],
        id_field= name_filed
    )

    template_repo = MemoryTemplateRepository()
    template_repo.get_template_by_id = lambda id: person_template
    template_repo.update_entity_of = lambda *args, **kwargs: True

    json_validator = ValidatorJsonSchema()
    update_entity_of_use_case = UpdateEntityOf(template_repo, json_validator)


    with pytest.raises(Exception):
        update_entity_of_use_case.run(
                [
                    DynamicValue(
                        "name", "Igor"),
                    DynamicField('like_pie', '099')
                ], ""
            )
