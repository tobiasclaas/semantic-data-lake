from http import HTTPStatus

from werkzeug.exceptions import BadRequest, HTTPException, NotFound, Conflict

from database.models import Annotation
from api.endpoints.ontologies import ask_query_fuseki


def create():
    """
    Creates a Annotation collection by adding a dummy entry and then removing it.
    """
    entity = Annotation(workspace_id='', datamart_id='', data_attribute='', ontology_attribute='')
    Annotation.objects().insert(entity)
    Annotation.objects(workspace_id='', datamart_id='', data_attribute='', ontology_attribute='').delete()


def get(workspace_id, datamart_id, data_attribute):
    """
    Get all annotations for data_attribute.
    """
    annotation: Annotation = Annotation.objects(workspace_id=workspace_id,
                                                datamart_id=datamart_id,
                                                data_attribute=data_attribute)
    if not annotation:
        return HTTPStatus.NOT_FOUND

    return annotation.get()


def add(workspace_id, datamart_id, data_attribute, property_description, ontology_attribute, comment=''):
    """
    Stores an annotation in MongoDB.
    :return:
    """
    ontology_tuple = [property_description, ontology_attribute]
    search_res = get(workspace_id, datamart_id, data_attribute)

    # TODO assure that datamart and data_attribute is a thing: CASE distinction where data is stored?

    # checks if ontology attribute exists
    query_res = ask_query_fuseki(workspace_id=workspace_id, subject_name=ontology_tuple[1])
    if not query_res or query_res is BadRequest:
        return HTTPStatus.BAD_REQUEST

    if search_res is HTTPStatus.NOT_FOUND:  # there are no annotations for data_attribute
        ontology_tuple = [ontology_tuple]
        entity = Annotation(workspace_id=workspace_id, datamart_id=datamart_id, data_attribute=data_attribute,
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
            Annotation.objects(workspace_id=workspace_id,
                               datamart_id=datamart_id,
                               data_attribute=data_attribute).update(ontology_attribute=attribute_annotation)
        except:
            return HTTPStatus.INTERNAL_SERVER_ERROR
    return HTTPStatus.CREATED


def delete(workspace_id, datamart_id, data_attribute, property_description, ontology_attribute):
    """
    Delete annotation of ontology_tuple for data_attribute.
    :return:
    """
    annotation_tuple = [property_description, ontology_attribute]

    entity = get(workspace_id, datamart_id, data_attribute)
    if entity is HTTPStatus.NOT_FOUND:
        return HTTPStatus.NOT_FOUND

    attribute_annotation = entity.ontology_attribute
    if annotation_tuple not in attribute_annotation:
        return HTTPStatus.BAD_REQUEST

    attribute_annotation.remove(annotation_tuple)
    # update document in collection
    try:
        if len(attribute_annotation) == 0:  # delete if there are no annotations for data_attribute
            Annotation.objects(workspace_id=workspace_id,
                               datamart_id=datamart_id,
                               data_attribute=data_attribute).delete()
        else:
            Annotation.objects(workspace_id=workspace_id,
                               datamart_id=datamart_id,
                               data_attribute=data_attribute).update(ontology_attribute=attribute_annotation)
    except:
        return HTTPStatus.INTERNAL_SERVER_ERROR

    return HTTPStatus.OK


# TODO delete, do with cascading delete
def delete_all(workspace_id, file_name, data_attribute):
    """
    Delete all annotations for a file.
    :return:
    """
    entity = get(workspace_id, file_name, data_attribute)
    if entity is HTTPStatus.NOT_FOUND:
        return HTTPStatus.NOT_FOUND

    try:
        Annotation.objects(workspace_id=workspace_id,
                           file_name=file_name,
                           data_attribute=data_attribute).delete()
        return HTTPStatus.OK
    except:
        return HTTPStatus.INTERNAL_SERVER_ERROR

