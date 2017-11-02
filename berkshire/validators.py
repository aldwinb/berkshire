from jsonschema import validate
from jsonschema.exceptions import ValidationError

GROUP_PUT_PAYLOAD_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
      'name': {
        'type': 'string'
      }
    }
}


def is_payload_valid(payload, schema):
    try:
        validate(payload, schema)
        is_valid = True
    except ValidationError:
        is_valid = False
    return is_valid
