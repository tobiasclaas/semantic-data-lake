from database.models import Datamart
from werkzeug.exceptions import NotFound


def get_by_uid(uid) -> Datamart:
    """
    Returns a datamart or raise NotFound Exception based on passed UID
    :param uid:
    :return: Datamart
    """
    datamart = Datamart.objects(uid__exact=uid)

    if not datamart:
        raise NotFound(f"Datamart with uid {uid} not found")

    return datamart.get()


def get_list(page, limit, field_to_order, asc, search):
    """
    Returns a list of datamarts, filtered by page, limit and other params
    :param page:
    :param limit:
    :param field_to_order:
    :param asc:
    :param search:
    :return: List of Datamarts
    """
    if search is None:
        return Datamart.objects\
            .order_by(field_to_order)\
            .paginate(page=page, per_page=limit)
    else:
        return Datamart.objects\
            .search_text(search)\
            .order_by(field_to_order)\
            .paginate(page=page, per_page=limit)
