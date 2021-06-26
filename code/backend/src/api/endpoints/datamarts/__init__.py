import json

from flask import jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful.reqparse import Argument
import requests
from api.services.decorators import parse_params
from business_logic.services.mapper import mapper
from database.data_access import datamart_data_access as data_access, user_data_access
from business_logic.spark import SparkHelper
from database.models import Datamart, CsvStorage, MongodbStorage
import settings


def process_input(spark_helper, data):
    """ input will be a json, return a datamart"""
    if "type" in data.keys() and data['type'] == 'join':
        df1 = process_input(spark_helper, data['input'][0]['input'][0])
        df2 = process_input(spark_helper, data['input'][1]['input'][0])
        dataframe = df1.join(df2, df1[data['input'][0]['column']] == df2[data['input'][1]['column']])
        return dataframe

    if "type" in data.keys() and data['type'] == 'filter':
        df1 = process_input(spark_helper, data['input'][0])
        dataframe = df1.filter(data["condition"])
        # Still need to write this functionalaiy
        return dataframe

    if "type" in data.keys() and data['type'] == 'select':
        df1 = process_input(spark_helper, data['input'][0])
        dataframe = df1.select(*data["columns"])
        return dataframe

    if "type" in data.keys() and data['type'] == 'source':
        datamart = data_access.get_by_uid(data['id'])
        dataframe = spark_helper.read_datamart(datamart)
        return dataframe

    # if "type" in data.keys() and data['type'] == 'source':
    #     print (data['type'] + ': ' + data['id'])
    #     return
    # elif "type" in data.keys():
    #     print("operation:" + data['type'])

    # print (process_input(spark_helper, data['input'][0]))


class Datamarts(Resource):
    @jwt_required
    @parse_params(
        Argument("page", default=1, type=int, required=False),
        Argument("limit", default=10, type=int, required=False),
        Argument("field_to_order", default="created_at", type=str, required=False),
        Argument("asc", default=False, type=bool, required=False),
        Argument("search", default=None, type=str, required=False),
        Argument("uid", default=None, type=str, required=False),
    )
    def get(self, page, limit, field_to_order, asc, search, uid=None):
        if uid is None:
            result = []
            datamarts = data_access.get_list(page, limit, field_to_order, asc, search)

            for datamart in datamarts.items:
                result.append(mapper(datamart))

            return jsonify({
                "total": datamarts.total,
                "datamarts": result
            })
        else:
            return jsonify(mapper(data_access.get_by_uid(uid)))

    @parse_params(
        Argument("uid", type=str, required=False),
    )
    def delete(self, uid):
        if uid == None:
            marts = Datamart.objects.all()
            for mart in marts:
                mart.delete()
            return f"All datamarts deleted"

        datamart = data_access.get_by_uid(uid)
        hnr = datamart.human_readable_name
        datamart.delete()
        return f"deleted datamart {hnr}"

    @jwt_required
    @parse_params(
        Argument("comment", default='', type=str, required=False),
        Argument("annotated_schema", required=False),
        Argument("human_readable_name", required=False),
    )
    def put(self, uid, comment, annotated_schema, human_readable_name):
        datamart = data_access.get_by_uid(uid)
        datamart.human_readable_name = human_readable_name
        datamart.comment = comment
        datamart.metadata.schema = annotated_schema \
            .replace("\'", "\"") \
            .replace(" ", "") \
            .replace("True", "true") \
            .replace("False", "false")
        datamart.save()
        return jsonify(mapper(datamart))

    @jwt_required
    @parse_params(
        Argument("op", type=str, required=True),
        Argument("mart1", type=str, required=True),
        Argument("mart2", default='', type=str, required=False),
    )
    def post(self, op, mart1, mart2):
        try:

            file = r"""{
               "type":"output",
               "name":"exported.csv",
               "target":"HDFS",
               "input":[
                  {
                     "type":"filter",
                     "condition":"name= \"Arsene Wenger\" or name= \"Robin Hood\"",
                     "input":[
                        {
                           "type":"select",
                           "columns":[
                              "name",
                              "dept_name",
                              "head"
                           ],
                           "input":[
                              {
                                 "type":"join",
                                 "input":[
                                    {
                                       "column":"Department",
                                       "input":[
                                          {
                                             "type":"source",
                                             "id":"1bb83ba0-a37b-44ee-9728-d8fb1524eef5"
                                          }
                                       ]
                                    },
                                    {
                                       "column":"id",
                                       "input":[
                                          {
                                             "type":"source",
                                             "id":"8739c272-cf67-40bf-91c9-2dcef57ffeb1"
                                          }
                                       ]
                                    }
                                 ]
                              }
                           ]
                        }
                     ]
                  }
               ]
            }"""
            # api_user = user_data_access.get_by_email(get_jwt_identity()["email"])

            data = json.loads(file)
            spark_helper = SparkHelper("transform")
            setting = settings.Settings()

            for data_input in data['input']:
                transformed_dataframe = process_input(spark_helper, data_input)
                storage = setting.mongodb_storage
                target_storage = MongodbStorage(
                    host=storage.host,
                    port=storage.port,
                    user=storage.user,
                    password=storage.password,
                    database=storage.database,
                    collection=data["name"]
                )
                spark_helper.write_mongodb(transformed_dataframe, target_storage)
                transformed_dataframe.show()

                spark_helper.spark_session.stop()

                paras = {
                    "host": storage.host,
                    "port": storage.port,
                    "database": storage.database,
                    "collection": data["name"],
                    "target_storage": data["target"],
                    "user": storage.user,
                    "password": storage.password,
                    "human_readable_name": data["name"]
                }
                headers = {'content-type': 'application/json', 'Cookie': "access_token_cookie"
                                                                         "=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
                                                                         ".eyJpYXQiOjE2MjI3MTA0MDcsIm5iZiI6MTYyMjcxMDQwNywianRpIjoiNDhmZjBhOWUtZjhiMC00MWU5LTllNzAtZGQyNTQ5ZGJjNzY0IiwiZXhwIjo5MTYyMjcxMDQwNywiaWRlbnRpdHkiOnsiZW1haWwiOiJhZG1pbiIsImZpcnN0bmFtZSI6IkFkbWluIiwibGFzdG5hbWUiOiJVc2VyIiwiaXNBZG1pbiI6dHJ1ZX0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.YnGpikBeOGlsvPaLyrtI-rvqLiuBYAoGcX-MdcdhQtU; refresh_token_cookie=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MjI3MTA0MDcsIm5iZiI6MTYyMjcxMDQwNywianRpIjoiZTAzYzQ5NDYtMTM4NS00NmM0LWEwMjgtNGUzYzgzNTM4NGYxIiwiZXhwIjo5MTYyMjcxMDQwNywiaWRlbnRpdHkiOnsiZW1haWwiOiJhZG1pbiIsImZpcnN0bmFtZSI6IkFkbWluIiwibGFzdG5hbWUiOiJVc2VyIiwiaXNBZG1pbiI6dHJ1ZX0sInR5cGUiOiJyZWZyZXNoIn0.dY9SFrmEJK1erv4KzXEJdAk0oYjR7tLm3r2nBgW9Ags"}
                # TODO dynamically get url of server
                requests.post(url="http://0.0.0.0:5000/datamarts/ingestion/mongodb", data=json.dumps(paras), headers=headers)

                #
                # if data["target"] == "HDFS":
                #
                #     datamart = create_datamart(api_user, None, target_storage, data["name"], '')
                #     resp = spark_helper.write_csv(transformed_dataframe, target_storage)


            return jsonify([200])

        except Exception as e:
            if (spark_helper):
                spark_helper.spark_session.stop()

            print(e)
