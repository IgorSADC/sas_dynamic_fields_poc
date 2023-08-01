from models.dynamic_field import FieldValidator


class CommonFieldValidators:
    no_number_validator = FieldValidator('pattern', '[^0-9]')