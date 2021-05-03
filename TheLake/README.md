# TheLake
Backend and API for the DataLake

## Routes: 

### Auth

| Method | URL                                                        | Comment |
| :----- | :--------------------------------------------------------- | :------ |
| POST   | http://127.0.0.1:5000/auth/login?data                      |
| POST   | http://127.0.0.1:5000/auth/register?data                   |
| POST   | http://127.0.0.1:5000/auth/logout                          |
| POST   | http://127.0.0.1:5000/auth/refresh                         |

__data :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| email                          | String  | email of user                                                     |
| password                       | String  | password of user                                                  |

### User

| Method | URL                                      | Comment                               |
| :----- | :--------------------------------------- | :-------------------------------------|
| GET    | http://127.0.0.1:5000/user               | returns list of all users             |
| GET    | http://127.0.0.1:5000/user/email         | returns given user                    |
| POST   | http://127.0.0.1:5000/user?data          | add user                              |
| PUT    | http://127.0.0.1:5000/user/email?data    | update data                           |
| DELETE | http://127.0.0.1:5000/user/email         | delete a user                         |

__data :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| email                          | String  | email of user                                                     |
| isAdmin                        | Boolean | true=admin, false=user                                            |
| firstname                      | String  | firstname of user                                                 |
| lastname                       | String  | lastname of user                                                  |

### MetaData

| Method | URL                                          | Comment                               |
| :----- | :------------------------------------------- | :-------------------------------------|
| GET    | http://127.0.0.1:5000/metaData               | returns list of all meta data entrys  |
| GET    | http://127.0.0.1:5000/metaData/uid?queryData | returns given user                    |
| PUT    | http://127.0.0.1:5000/metaData/uid?data      | update data                           |
| DELETE | http://127.0.0.1:5000/metaData/uid           | delete a meta data entry              |

__queryData :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| page                           | Int     | always starts at 1 not 0                                          |
| asc                            | Boolean | asc=True; asc=False => desc                                       |
| limit                          | Int     | limit of entry per page, default is 10 entry per page             |
| fieldToOrder                   | String  | name of field what will be used for ordering/sorting              |

__data :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| comment                        | String  | further informations of meta data entry                           |
| shema                          | String  | schema with annotations                                           |

### Job

| Method | URL                                          | Comment                               |
| :----- | :------------------------------------------- | :-------------------------------------|
| GET    | http://127.0.0.1:5000/job                    | returns list of all jobs              |
| GET    | http://127.0.0.1:5000/job/uid?queryData      | returns given job                     |
| DELETE | http://127.0.0.1:5000/job/uid                | delete a job                          |

__queryData :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| page                           | Int     | always starts at 1 not 0                                          |
| asc                            | Boolean | asc=True; asc=False => desc                                       |
| limit                          | Int     | limit of entry per page, default is 10 entry per page             |
| fieldToOrder                   | String  | name of field what will be used for ordering/sorting              |

### Ingestion

| Method | URL                                                  | Comment                               |
| :----- | :--------------------------------------------------- | :-------------------------------------|
| POST   | http://127.0.0.1:5000/ingestion/file?fileData        | ingestion of file                     |
| POST   | http://127.0.0.1:5000/ingestion/mongodb?mongoData    | ingestion of mongodb                  |
| POST   | http://127.0.0.1:5000/ingestion/postgres?postgresData| ingestion of postgres                 |

__fileData :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| file                           | File    | source                                                            |
| delimiter                      | String  | if a csv is uploaded a delimiter should be given                  |
| hasHeader                      | Boolean | if a csv is uploaded the flag must be defined                     |
| targetStorageSystem            | String  | valid options are: [HDFS, PostgreSQL, MongoDB]                    |
| comment                        | String  | further informations for meta data entry                          |
| humanReadableName              | String  | readable name for meta data entry                                 |

__mongoData :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| host                           | String  | host from source db                                               |
| port                           | String  | port from source db                                               |
| database                       | String  | dbname from source db                                             |
| collection                     | String  | collection from source db that should be used                     |
| user                           | String  | username from source db                                           |
| password                       | String  | password from source db                                           |
| targetStorageSystem            | String  | valid options are: [HDFS, PostgreSQL, MongoDB]                    |
| comment                        | String  | further informations for meta data entry                          |
| humanReadableName              | String  | readable name for meta data entry                                 |

__postgresData :__

| Key                            | Type    | Comment                                                           |
| :----------------------------- | :------ | :---------------------------------------------------------------- |
| host                           | String  | host from source db                                               |
| port                           | String  | port from source db                                               |
| database                       | String  | dbname from source db                                             |
| table                          | String  | tablename from source db that should be used                      |
| user                           | String  | username from source db                                           |
| password                       | String  | password from source db                                           |
| targetStorageSystem            | String  | valid options are: [HDFS, PostgreSQL, MongoDB]                    |
| comment                        | String  | further informations for meta data entry                          |
| humanReadableName              | String  | readable name for meta data entry                                 |

## Installation

If you want to work without the frontend you can do so and use this postman collection: https://www.getpostman.com/collections/a46c0b06c91af361fed4 
### Without Docker

To run the backend python 3.9 is required. 

- python3 -m pip install -r requirements.txt
- python3 server.py

### With Docker

- docker-compose up
