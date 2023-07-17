

import re

import pytest
from exceptions.custom_exceptions import FieldNotFoundInTemplateException, ValidationFailedException
from models.dynamic_field import DynamicField, DynamicFieldSignature, DynamicValue
from models.template import DynamicTemplate
from use_case.create_entity_of import CreateEntityOf


class Mock:
    pass


def test_can_create_entity():
    validator = Mock()
    validator.is_valid = lambda name: not re.match("[0-9]", name)
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )

    person_template = DynamicTemplate(
        'person_template',
        [name_filed]
    )

    template_repo = Mock()
    template_repo.get_template_by_id = lambda id: person_template

    create_entity_of_use_case = CreateEntityOf(template_repo)

    create_entity_of_use_case.run(
        [
            DynamicValue(
                "name", "Igor")
        ], ""
    )


def test_cannot_create_if_template_validation_fails():
    validator = Mock()
    validator.is_valid = lambda name: not re.match("[0-9]", name)
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )

    person_template = DynamicTemplate(
        'person_template',
        [name_filed]
    )

    template_repo = Mock()
    template_repo.get_template_by_id = lambda id: person_template

    create_entity_of_use_case = CreateEntityOf(template_repo)

    with pytest.raises(ValidationFailedException):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "3321")
            ], ""
        )


def test_can_skip_optional_fields():
    validator = Mock()
    validator.is_valid = lambda name: not re.match("[0-9]", name)
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
        [name_filed, last_name_field]
    )

    template_repo = Mock()
    template_repo.get_template_by_id = lambda id: person_template

    create_entity_of_use_case = CreateEntityOf(template_repo)

    create_entity_of_use_case.run(
        [
            DynamicValue(
                "name", "Igor")
        ], ""
    )


def test_cant_pass_invalid_optional_field():
    validator = Mock()
    validator.is_valid = lambda name: not re.match("[0-9]", name)
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
        [name_filed, last_name_field]
    )

    template_repo = Mock()
    template_repo.get_template_by_id = lambda id: person_template

    create_entity_of_use_case = CreateEntityOf(template_repo)

    with pytest.raises(ValidationFailedException):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "Igor"),
                DynamicValue(
                    "last_name", "3234"),

            ], ""
        )

def test_cannot_pass_non_templated_field():
    validator = Mock()
    validator.is_valid = lambda name: not re.match("[0-9]", name)
    name_filed = DynamicField(
        'name',
        DynamicFieldSignature(True, True),
        validator

    )

    person_template = DynamicTemplate(
        'person_template',
        [name_filed]
    )

    template_repo = Mock()
    template_repo.get_template_by_id = lambda id: person_template

    create_entity_of_use_case = CreateEntityOf(template_repo)

    with pytest.raises(FieldNotFoundInTemplateException):
        create_entity_of_use_case.run(
            [
                DynamicValue(
                    "name", "Igor"),
                DynamicValue(
                        "last_name", "Costa")
            ], ""
        )