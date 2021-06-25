from http import HTTPStatus

import json
import uuid
from bson.binary import Binary, UuidRepresentation
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Conflict

from database.models import Annotation, Datamart
from api.endpoints.ontologies import ask_query_fuseki


def check_data_attribute(datamart_id, data_attribute):
    """
    Checks if data_attribute exists for datamart.
    :return: True if exists, False if not exists.
    """
    datamart = Datamart.objects(uid=datamart_id).get()
    if not datamart:
        return HTTPStatus.NOT_FOUND
    entries = json.loads(datamart.metadata.schema)['fields']
    for entry in entries:
        if entry['name'] == data_attribute:
            return True
    return False


def get(datamart_id, data_attribute):
    """
    Get all annotations for data_attribute.
    """
    annotation: Annotation = Annotation.objects(datamart_id=datamart_id,
                                                data_attribute=data_attribute)
    if not annotation:
        return HTTPStatus.NOT_FOUND

    return annotation.get()


def add(workspace_id, datamart_id, data_attribute, property_description, ontology_attribute, comment=''):
    """
    Stores an annotation in MongoDB.
    :return: according HTTP status
    """
    # checks if data_attribute exists
    if not check_data_attribute(datamart_id, data_attribute):
        return BadRequest

    # checks if ontology attribute exists
    query_res = ask_query_fuseki(workspace_id=workspace_id, subject_name=ontology_attribute)
    if not query_res or query_res is BadRequest:
        return HTTPStatus.BAD_REQUEST

    search_res = get(datamart_id, data_attribute)
    ontology_tuple = [property_description, ontology_attribute]
    if search_res is HTTPStatus.NOT_FOUND:  # there are no annotations for data_attribute
        ontology_tuple = [ontology_tuple]
        entity = Annotation(datamart_id=datamart_id, data_attribute=data_attribute,
                            ontology_attribute=ontology_tuple, comment=comment)
        try:
            Annotation.objects.insert(entity)
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    else:  # there exists some annotation for data_attribute
        # append new annotation to list
        if ontology_tuple in search_res.ontology_attribute:
            return HTTPStatus.BAD_REQUEST

        attribute_annotation = search_res.ontology_attribute
        attribute_annotation.append(ontology_tuple)
        # update document in collection
        try:
            Annotation.objects(datamart_id=datamart_id,
                               data_attribute=data_attribute).update(ontology_attribute=attribute_annotation)
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    return HTTPStatus.CREATED


def delete(datamart_id, data_attribute, property_description, ontology_attribute):
    """
    Delete annotation of ontology_tuple for data_attribute.
    :return:
    """
    annotation_tuple = [property_description, ontology_attribute]

    entity = get(datamart_id, data_attribute)
    if entity is HTTPStatus.NOT_FOUND:
        return HTTPStatus.NOT_FOUND

    attribute_annotation = entity.ontology_attribute
    if annotation_tuple not in attribute_annotation:
        return HTTPStatus.BAD_REQUEST

    attribute_annotation.remove(annotation_tuple)
    # update document in collection
    try:
        if len(attribute_annotation) == 0:  # delete if there are no annotations for data_attribute
            Annotation.objects(datamart_id=datamart_id,
                               data_attribute=data_attribute).delete()
        else:
            Annotation.objects(datamart_id=datamart_id,
                               data_attribute=data_attribute).update(ontology_attribute=attribute_annotation)
    except:
        return HTTPStatus.INTERNAL_SERVER_ERROR

    return HTTPStatus.OK
