"""Request Validator

This script allows validating requests (via the `requests` library) to be validated
against OpenAPI API documentation.
"""

import yaml
import responses
import os
from functools import wraps

from openapi_core import Spec
from openapi_core import validate_response as vres, validate_request as vreq
from openapi_core.contrib.requests import RequestsOpenAPIRequest, RequestsOpenAPIResponse

dirname = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(dirname, '../documentation/pollapi.yaml')
with open(filename, 'r') as spec_file:
    spec_dict = yaml.load(spec_file, yaml.SafeLoader)
    spec_dict['servers'][0]['url'] = 'https://example.com/index.php/apps/polls/api/v1.0'
spec = Spec.from_dict(spec_dict)


def validate_request(func):
    """Validates all requests and responses after the wrapped function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        for call in responses.calls:
            req = RequestsOpenAPIRequest(call.request)
            vreq(req, spec=spec)

            res = RequestsOpenAPIResponse(call.response)
            vres(req, res, spec=spec)
    return wrapper
