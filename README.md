The core for the APP is on the template engine that is responsible for registering runtime fields and rules. A template is a collection of custom fields with their own validation

the pseudo code to validate a template is: 
requires = 0
For each field in request: 
    if field not in template: raise Exception("Field don't exist")
    template[field].validate(field)
    if template[field].required
        requires += 1

if template.required_count < requires: 
    raise Exception("Missing required field")


Notice that the algorithm changes over operations. For example an edit would be:

For each field in request: 
    if field not in template: raise Exception("Field don't exist")
    if field.frozen: raise Exception("Cannot edit frozen field")
    template[field].validate(field) #may raise an invalid field exception


The engine support template casting, aka views: 

template_one = { 
    "name"
}

template_two = {
    "name",
    "address"
}


template_two can be castable to template one.

def is_template_castable(t1, t2): 
    for field in t1: 
        if not field.required : continue
        if field not in t2: 
            return False

    return True