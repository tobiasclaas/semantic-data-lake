from http import HTTPStatus

from database.models import Annotation


def get(workspace_id, file_name, data_attribute) -> [Annotation]:
    """
    Get all annotations for data_attribute.
    """
    annotation: Annotation = Annotation.objects(workspace_id=workspace_id,
                                                file_name=file_name,
                                                data_attribute=data_attribute)

    if not annotation:
        raise HTTPStatus.NOT_FOUND

    return annotation.get()


def add(workspace_id, file_name, data_attribute, ontology_attribute, comment=''):
    """
    Stores an annotation in MongoDB.
    :return:
    """
    # TODO check if annotation already exists
    # a = Annotation.objects(workspace_id=workspace_id, file_name=file_name,
    #                       data_attribute=data_attribute, ontology_attribute=ontology_attribute).get()
    # print(a)

    entity = Annotation(workspace_id=workspace_id, file_name=file_name, data_attribute=data_attribute,
                        ontology_attribute=ontology_attribute, comment=comment)
    a = Annotation.objects.insert(entity)
    print(type(a))

    return HTTPStatus.CREATED


def delete(workspace_id, file_name, data_attribute, ontology_attribute):
    """
    Delete annotation of ontology_attribute for data_attribute.
    :param workspace_id:
    :param file_name:
    :param data_attribute:
    :param ontology_attribute:
    :return:
    """
    Annotation.objects(workspace_id=workspace_id, file_name=file_name,
                       data_attribute=data_attribute, ontology_attribute=ontology_attribute).delete()


def delete_all(workspace_id, file_name, data_attribute):
    """
    Delete all annotations for a file.
    :param workspace_id:
    :param file_name:
    :param data_attribute:
    :return:
    """
    pass
