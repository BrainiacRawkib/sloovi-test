"""List of responses returned by all apps views."""
from flask import jsonify


""" Custom Generic Responses """

def custom_http_response(code, *args, **kwargs):
    return jsonify(*args, **kwargs), code


""" 2xx Responses: Success """

def http_response_200(*args, **kwargs):
    return jsonify(*args, **kwargs), 200


def http_response_201(*args, **kwargs):
    return jsonify(*args, **kwargs), 201


def http_response_204(*args, **kwargs):
    return jsonify(*args, **kwargs), 204


""" 4xx Responses: Client Errors """

def http_response_400(*args, **kwargs):
    return jsonify(*args, **kwargs), 400


def http_response_401(*args, **kwargs):
    return jsonify(*args, **kwargs), 401


def http_response_403(*args, **kwargs):
    return jsonify(*args, **kwargs), 403


def http_response_404(*args, **kwargs):
    return jsonify(*args, **kwargs), 404


def http_response_406(*args, **kwargs):
    return jsonify(*args, **kwargs), 406


def http_response_409(*args, **kwargs):
    return jsonify(*args, **kwargs), 409


def http_response_422(*args, **kwargs):
    return jsonify(*args, **kwargs), 422


def http_response_429(*args, **kwargs):
    return jsonify(*args, **kwargs), 429


""" 5xx Responses: Server Errors """

def http_response_500(*args, **kwargs):
    return jsonify(*args, **kwargs), 500


def http_response_502(*args, **kwargs):
    return jsonify(*args, **kwargs), 502
