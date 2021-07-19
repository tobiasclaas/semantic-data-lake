import datetime
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask_api import status
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import Argument
from werkzeug.exceptions import NotFound, InternalServerError
from flask import jsonify

from api.services.decorators import parse_params
from utils.services.create_datamart import create_datamart
from utils.spark import SparkHelper
from database.data_access import datamart_data_access, user_data_access
from database.models import Datamart, DatamartState
from settings import Settings
from utils.services.mapper import mapper

STATE_RUNNING = 1
STATE_FINISHED = 2
STATE_FAILED = 3

session_states = {}

settings = Settings()


class SessionStore:
    STATES = ["", "running", "finished", "failed"]

    def __init__(self):
        self.state: int = STATE_FINISHED
        self.error: str = ""
        self.construction_code: str = ""
        self.construction_query: str = ""

    def mapped(self):
        return {
            "state": self.STATES[self.state],
            "error": self.state,
            "constructionCode": self.construction_code,
            "constructionQuery": self.construction_query
        }


def get_state(email) -> SessionStore:
    state = None
    
    try:
        state = session_states[email]
    except: 
        pass

    if not state:
        state = SessionStore()
        session_states[email] = state
    return state


# ==================================================================================================
# preview api
# ==================================================================================================
class DatamartPreviewApi(Resource):
    def __generate_preview(self, email, datamarts, pyspark, query):
        session_state = get_state(email)

        try:
            spark_helper = SparkHelper(f"creation_{email}")

            # load all dataframes
            for identifier, datamart_id in datamarts.items():
                datamart = datamart_data_access.get_by_uid(datamart_id)
                exec(f"{identifier} = spark_helper.read_datamart(datamart)")

            if pyspark:
                exec(pyspark)

            for identifier, datamart_id in datamarts.items():
                exec("{0}.createOrReplaceTempView('{0}')".format(identifier))

            dataframe = spark_helper.spark_session.sql(query)
            dataframe.createOrReplaceTempView("result")
            session_state.construction_code = pyspark
            session_state.construction_query = query
            session_state.state = STATE_FINISHED
        except Exception as err:
            session_state.error = err
            session_state.state = STATE_FAILED

    @jwt_required
    @parse_params(
        Argument("preview_row_count", type=int, default=10),
    )
    def get(self, preview_row_count: int):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
        session_state = get_state(api_user.email)

        if not session_state:
            raise NotFound("No session for user found")

        # still generating preview
        if session_state.state == STATE_RUNNING:
            return f"generating preview", status.HTTP_202_ACCEPTED

        elif session_state.state == STATE_FAILED:
            response: dict = {
                "message": f"generating preview failed:\n{session_state.error}"
            }
            return response, status.HTTP_400_BAD_REQUEST

        # preview generated
        elif session_state.state == STATE_FINISHED:
            spark_helper = SparkHelper(f"creation_{api_user.email}")
            dataframe = spark_helper.spark_session.sql("SELECT * FROM result")
            response: dict = {
                "schema": dataframe.schema.jsonValue(),
                "rows": dataframe.head(preview_row_count)
            }
            return response, status.HTTP_201_CREATED

    @jwt_required
    @parse_params(
        Argument("datamarts", type=dict, required=True),
        Argument("pyspark", type=str),
        Argument("query", type=str, required=True),
    )
    def post(self, datamarts, pyspark, query):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
        session_state = get_state(api_user.email)

        if not session_state:
            raise NotFound("No session for user found")

        if session_state.state == STATE_RUNNING:
            return f"generating preview", status.HTTP_202_ACCEPTED

        else:
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                lambda: self.__generate_preview(api_user.email, datamarts, pyspark, query))
            session_state.state = STATE_RUNNING
            scheduler.start()
            return f"generating preview", status.HTTP_200_OK


# ==================================================================================================
# save api
# ==================================================================================================
class DatamartSaveApi(Resource):

    @jwt_required
    @parse_params(
        Argument("datamarts", required=True, action="append"),
        Argument("human_readable_name", type=str, required=True),
        Argument("comment", type=str),
        Argument("target_storage", type=str),
    )
    def post(
            self, datamarts, human_readable_name, comment, target_storage,
    ):
        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])
        session_state = get_state(api_user.email)

        if not session_state:
            raise NotFound("No session for user found")

        if session_state.state == STATE_RUNNING:
            return f"generating preview", status.HTTP_405_METHOD_NOT_ALLOWED

        spark_helper = SparkHelper(f"creation_{api_user}")
        dataframe = spark_helper.spark_session.sql("SELECT * FROM result")

        heritage = []
        for uid in datamarts:
            datamart: Datamart = datamart_data_access.get_by_uid(uid)
            heritage.append(datamart)

        api_user = user_data_access.get_by_email(get_jwt_identity()["email"])

        datamart = create_datamart(api_user, None, target_storage, human_readable_name, comment)
        datamart.status.started = datetime.datetime.now()

        try:
            spark_helper.write_datamart(datamart, dataframe)
        except Exception as e:
            datamart.delete()
            raise InternalServerError()

        datamart.status.state = DatamartState.SUCCESS
        datamart.status.ended = datetime.datetime.now()
        datamart.save()

        spark_helper.spark_session.stop()

        return jsonify(mapper(datamart))
