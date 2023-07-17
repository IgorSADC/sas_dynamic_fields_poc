from models.template import DynamicTemplate


def validate_template(template : DynamicTemplate):
    for t in template.attributes: 
        if not t.Validator.is_valid(t.Value.value):
            return False
        
    return True