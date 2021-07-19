import json
from requests import post
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, InternalServerError, Conflict
from database.models import Annotation, Datamart
import settings


def ask_query_fuseki(workspace_id, subject_name):
    """
    Performs ask query on Fuseki Default-Graph. Checks if an entry with a specified subject exists.

    :param workspace_id: to identify dataset in fuseki.
    :param subject_name: name of subject to be searched.
    :return: True if such an entry exists, false otherwise.
    """
    query_string = "ASK { " + subject_name + " ?p ?o . }"
    # replace admin and pw by environment variable defined in docker-compose.yaml
    p = post('http://localhost:3030/' + workspace_id, auth=(settings.Settings().fuseki_storage.user,
                                                            settings.Settings().fuseki_storage.password),
             data={'query': query_string})

    try:
        return json.loads(p.content)["boolean"]
    except:
        raise InternalServerError


def check_data_attribute(datamart_id, data_attribute):
    """
    Checks if data_attribute exists for datamart.

    :param datamart_id: id of datamart.
    :param data_attribute: name of attribute/column to be annotated.
    :return: True if exists, False if not exists.
    """
    datamart = Datamart.objects(uid=datamart_id)
    if len(datamart) == 0:
        raise NotFound  # Datamart not found
    datamart = datamart.get()
    if not datamart.metadata.source.has_header:
        return False  # file has no header

    entries = json.loads(datamart.metadata.schema)['fields']
    for entry in entries:
        if entry['name'] == data_attribute:
            return True
    return False


def get(datamart_id, data_attribute):
    """
    Get all annotations for data_attribute.

    :param datamart_id: id of datamart.
    :param data_attribute: name of attribute/column to be annotated.
    """

    try:
        if data_attribute is None:
            annotation: Annotation = Annotation.objects(datamart_id=datamart_id)
        else:
            annotation: Annotation = Annotation.objects(datamart_id=datamart_id,
                                                        data_attribute=data_attribute)
    except:
        raise NotFound

    return annotation.all()


def perform_integrity_checks(workspace_id, datamart_id, data_attribute, ontology_attribute):
    """
    Calls all manual integrity checks and checks their results.

    :param workspace_id: id of workspace.
    :param datamart_id: id of datamart.
    :param data_attribute: name of attribute/column to be annotated.
    :param ontology_attribute: attribute of ontology that provides semantic knowledge for data_attribute
    :return: None or raises error
    """
    # checks if data_attribute exists
    # if not check_data_attribute(datamart_id, data_attribute):
    #    raise NotFound

    # checks if ontology attribute exists
    query_res = ask_query_fuseki(workspace_id=workspace_id, subject_name=ontology_attribute)
    if not query_res:
        raise NotFound

    return None


def add(workspace_id, datamart_id, data_attribute, property_description, ontology_attribute, comment=''):
    """
    Stores an annotation in MongoDB if all integrity checks are passed. Case distinction if entry with workspace_id and
    datamart_id already exists or not.

    :param workspace_id: id of workspace
    :param datamart_id: id of datamart which contains data_attribute
    :param data_attribute: column to be annotated
    :param property_description: description of the annotation
    :param ontology_attribute: attribute of ontology that provides semantic knowledge for data_attribute
    :param comment: comment: A comment, may give some information about the datamart or the status of the annotation or
            ontologies that are used.
    :return: The updated or unchanged entity.
    """
    perform_integrity_checks(workspace_id, datamart_id, data_attribute, ontology_attribute)

    ontology_tuple = [property_description, ontology_attribute]

    try:  # there exists some annotation for data_attribute
        old_annotation_entity = get(datamart_id, data_attribute)

        if len(old_annotation_entity) == 0:  # just add the new entry
            ontology_tuple = [ontology_tuple]
            entity = Annotation(datamart_id=datamart_id, data_attribute=data_attribute,
                                ontology_attribute=ontology_tuple, comment=comment)
            try:
                Annotation.objects.insert(entity)
                return entity
            except:
                raise InternalServerError

        old_annotation_entity = old_annotation_entity.get()

        # check if annotation exists
        if ontology_tuple in old_annotation_entity.ontology_attribute:
            return old_annotation_entity

        # append new annotation to list
        attribute_annotation = old_annotation_entity.ontology_attribute
        attribute_annotation.append(ontology_tuple)

        # update document in collection
        try:
            if comment == '':  # comment is not modified
                Annotation.objects(datamart_id=datamart_id,
                                   data_attribute=data_attribute).update(ontology_attribute=attribute_annotation)
            else:
                Annotation.objects(datamart_id=datamart_id,
                                   data_attribute=data_attribute).update(ontology_attribute=attribute_annotation,
                                                                         comment=comment)
        except:
            raise InternalServerError

        return Annotation.objects(datamart_id=datamart_id,
                                  data_attribute=data_attribute,
                                  ontology_attribute=attribute_annotation).get()

    except HTTPException as ex:  # there are no annotations for data_attribute
        raise InternalServerError


def delete(datamart_id, data_attribute, ontology_attribute):
    """
    Deletes a the annotation of data_attribute with ontology-attribute ontology_attribute.

    :param datamart_id: id of datamart which contains data_attribute.
    :param data_attribute: selected column.
    :param ontology_attribute: annotation for column.
    :returns: updated entry.
    """
    entity = get(datamart_id, data_attribute)
    if len(entity) == 1:
        attribute_annotation = entity.get().ontology_attribute
    else:  # len(entity) > 1
        attribute_annotation = [entity[i].ontology_attribute for i in range(0, len(entity))]

    # attribute_annotation = entity.ontology_attribute  # list of tuple (description., ontology_attr.)
    new_attribute_annotation = [x for x in attribute_annotation if not x[1] == ontology_attribute]

    if len(attribute_annotation) == len(new_attribute_annotation):  # check if something changed
        return entity

    # update document in collection
    try:
        if len(new_attribute_annotation) == 0:  # delete if there are no annotations for data_attribute
            Annotation.objects(datamart_id=datamart_id,
                               data_attribute=data_attribute).delete()
            return None
        else:
            Annotation.objects(datamart_id=datamart_id,
                               data_attribute=data_attribute).update(ontology_attribute=attribute_annotation)
            return Annotation.objects(datamart_id=datamart_id,
                                      data_attribute=data_attribute).all()
    except:
        raise InternalServerError
