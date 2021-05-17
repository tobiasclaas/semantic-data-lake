# Api

## Auth
| Path   | Method | Parameters | Description |
| :----- | :----- | :--------- | :----- |
| /auth/login | POST | email<br>password | login |
| /auth/logout | POST | | logout |
| /auth/token_refresh | POST | | refresh jwt token |

## Users
| Path   | Method | Parameters | Description |
| :----- | :----- | :--------- | :----- |
| /users | GET | | get all users|
| /users/<email> | GET | | get user by email |
| /users | PUT | email<br>firstname<br>lastname<br>is_admin | updates user with email |
| /users | POST | email<br>password<br>firstname<br>lastname<br>is_admin | creates new user |
| /users | DELETE | email | deletes user
| /users/current | GET | | get authenticated user |

## Datamarts
| Path   | Method | Parameters | Description |
| :----- | :----- | :--------- | :----- |
| /datamarts | GET | page<br>limit<br>field_to_order<br>asc<br>search | list of datamarts |
| /datamarts | PUT | uid<br>comment<br>annotated_schema<br>human_readable_name | update datamart with uid | 
| /datamarts/<uid> | GET | uid | datamart by uid | 
| /datamarts/ingestion/mongodb | POST | host<br>port<br>database<br>collection<br>target_storage<br>user<br>password<br>comment<br>human_readable_name | ingest mongodb |
| /datamarts/ingestion/postgresql | POST | host<br>port<br>database<br>table<br>target_storage<br>user<br>password<br>comment<br>human_readable_name | ingest postgresql |
| /datamarts/ingestion/csv | POST | file<br>delimiter<br>has_header<br>target_storage<br>comment<br>human_readable_name | ingest data from csv file
| /datamarts/ingestion/json | POST | file<br>target_storage<br>comment<br>human_readable_name | ingest data from json file
| /datamarts/ingestion/xml | POST | file<br>row_tag<br>target_storage<br>comment<br>human_readable_name | ingest data from xml file
| /datamarts/creation/session | GET | | get creation session for user |
| /datamarts/creation/preview | GET | preview_row_count | get preview for session |
| /datamarts/creation/preview | POST | datamarts<br>pyspark<br>query | starts generating of preview |
| /datamarts/creation/save | POST | datamarts<br>human_readable_name<br>comment<br>target_storage | saves new datamart