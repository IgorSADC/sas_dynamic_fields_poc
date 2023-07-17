class MissingRequiredFieldException(Exception) : pass

class ValidationFailedException(Exception) : pass


class FieldNotFoundInTemplateException(Exception): pass

class FrozenFieldCannotBeEditedException(Exception): pass