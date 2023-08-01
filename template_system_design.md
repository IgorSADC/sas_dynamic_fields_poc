# Templating models
- CustomField {
    - type 
    - required
    - editable
    - Optional[CustomValidator]
}

- CustomValidator {
    - callable
}

- Template {
    List[CustomFields]
    EntityName
}

# Template Use cases
- RegisterTemplate
    * The template cannot repeat the same field.
    * You can register multiple templates for the same entity
    * You can't conflict the field type with a different template eg. you cant say english level is an integer in one and a string in other.This is not a problem for the engine, it's just to guarantee our users won't shoot themselves in the foot
- DeleteTemplate
    * The template needs to be registered 
    * This doesn't delete any data (?)
- GetTemplateById
- CreateEntityOf
    * Every required field needs to be passed. 
    * Unique fields cannot be repeated (ids).
    * Every field needs to pass the custom validator constraints.
- UpdateEntityOf
    * Cannot edit non editable fields. 
    * Every field needs to pass the custom validator constraints
- ListEntitiesOf
    * The template needs to be registered
- ListEntitiesOutsideOf
    * The template needs to be registered
- DeleteEntitiyOf
    * This is a logical delete 
    * The template acts like a filter for deletion

**The validations should be done by the adapter since mongodb does that "for free".**

Person System 
Owns the "Person" entity templates.
Exposes APIs for CRUD persons.

Job System
Owns the "Job" entity templates.
Exposes APIs for CRUD jobs.

...


PersonSystem UseCase PseudoCode: 

def create_person(person_request, template_id = None):
    if not template_id:
        template = get_main_active_template()
    else:
        template = get_template_by_id(template_id)

    is_request_valid = TemplateValidatorRepository.validate(person_request, template)

    if not is_request_valid: 
        raise InvalidTemplate(TemplateError.from(person_request, template))

    return create_entity_of(person_request, template)
