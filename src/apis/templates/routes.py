from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from apis import users_collection, templates_collection
from apis.utils import responses
from apis.utils.error_logger import logger

from . import templates


BASE_URL = '/templates'


@templates.route(f'{BASE_URL}/create_template', methods=['POST'])
@jwt_required()
def templates_create_template():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()

        user = users_collection.find_one({'email': current_user})
        if not user:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'User not found!'
            })

        new_template = {
            'template_name': data['template_name'],
            'subject': data['subject'],
            'body': data['body'],
            'user': user['email']
        }

        # create new template
        templates_collection.insert_one(new_template)

        return responses.http_response_201({
            'status': 'success',
            'msg': 'Template created!'
        })
    except Exception as e:
        logger.error('templates_create_template@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })


@templates.route(f'{BASE_URL}', methods=['GET'])
@jwt_required()
def templates_get_all_templates_route():
    try:
        current_user = get_jwt_identity()
        user = users_collection.find_one({'email': current_user})

        # get template
        templates = templates_collection.find({'user': user['email']})

        template_data = []
        for template in templates:
            template_data.append({
                'id': f"{template['_id']}",
                'template_name': template['template_name'],
                'subject': template['subject'],
                'body': template['body']
            })

        return responses.http_response_200({
            'status': 'success',
            'msg': 'Templates retrieved!',
            'data': template_data
        })
    except Exception as e:
        logger.error('templates_get_all_templates_route@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })


@templates.route(f'{BASE_URL}/<string:template_id>', methods=['GET'])
@jwt_required()
def templates_get_template_route(template_id: str):
    try:
        try:
            # convert string id to ObjectId
            object_id = ObjectId(template_id)
        except InvalidId:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Invalid ObjectID'
            })
        current_user = get_jwt_identity()

        # retrieve user of the post
        user = users_collection.find_one({'email': current_user})

        # get template for author
        template = templates_collection.find_one({'_id': object_id, 'user': user['email']})
        if not template:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Template not found!'
            })

        template_data = {
            'template_name': template['template_name'],
            'subject': template['subject'],
            'body': template['body'],
            'user': template['user']
        }
        return responses.http_response_200({
            'status': 'success',
            'msg': 'Template retrieved!',
            'data': template_data

        })
    except Exception as e:
        logger.error('templates_get_template_route@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })


@templates.route(f'{BASE_URL}/<string:template_id>/update', methods=['PUT'])
@jwt_required()
def templates_update_template_route(template_id: str):
    try:
        try:
            # convert string id to ObjectId
            object_id = ObjectId(template_id)
        except InvalidId:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Invalid ObjectID'
            })

        current_user = get_jwt_identity()
        data = request.get_json()

        # retrieve user
        user = users_collection.find_one({'email': current_user})
        if not user:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'User not found!'
            })

        # get template for author
        template = templates_collection.find_one({'_id': object_id, 'user': user['email']})
        if not template:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Template not found!'
            })

        updated_template = {
            'template_name': data['template_name'],
            'subject': data['subject'],
            'body': data['body']
        }

        # create new template
        templates_collection.update_one(template, {'$set': updated_template})

        return responses.http_response_200({
            'status': 'success',
            'msg': 'Template updated!'
        })
    except Exception as e:
        logger.error('templates_update_template_route@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })


@templates.route(f'{BASE_URL}/<string:template_id>/delete', methods=['DELETE'])
@jwt_required()
def templates_delete_template_route(template_id: str):
    try:
        try:
            # convert string id to ObjectId
            object_id = ObjectId(template_id)
        except InvalidId:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Invalid ObjectID'
            })

        current_user = get_jwt_identity()

        # retrieve user
        user = users_collection.find_one({'email': current_user})
        if not user:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'User not found!'
            })

        # get template for author
        template = templates_collection.find_one({'_id': object_id, 'user': user['email']})
        if not template:
            return responses.http_response_404({
                'status': 'failed',
                'msg': 'Template not found!'
            })

        # create new template
        templates_collection.delete_one(template)
        return responses.http_response_204({
            'status': 'success',
            'msg': 'Template deleted!'
        })
    except Exception as e:
        logger.error('templates_delete_template_route@Error')
        logger.error(e)
        return responses.http_response_500({
            'status': 'failed',
            'msg': 'An error occurred!'
        })
