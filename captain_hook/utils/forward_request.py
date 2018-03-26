import requests
from flask import Response


def forward_request(endpoint, request):
    method = request.method.lower()
    func = getattr(requests, method)
    headers = {}
    for key, val in enumerate(request.headers.to_list()):
        headers[val[0]] = val[1]

    print endpoint
    print method

    r = func(endpoint, data=request.get_data(), headers=headers)
    response = Response(r.content, r.status_code)
    response.headers = r.headers.items()
    return response
