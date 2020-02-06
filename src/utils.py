def validate_input(data):
    test_value = []
    errors = []
    
    EXPECTED_FEATURES = ("City", "State", "input-type", "kw_or_beer")
    
    if not data:
        errors.append("Form data must not be empty")
    else:
        for feature in EXPECTED_FEATURES:
            if feature not in data:
                errors.append(f"'{feature}' is a required field")
            else:
                try:
                    test_value.append(str(data[feature]))
                except ValueError:
                    errors.append(f"Invalid value for field {feature}: '{data[feature]}'")

    return test_value, errors


    
