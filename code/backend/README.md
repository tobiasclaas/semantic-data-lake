# Backend for the Data-Lake

## General 

For this project Python 3.9 was used. A list of all used packages can be found in the following file: /Pipfile /requirements.txt

## Architecture

To better separate the individual logics and make them more independent, a three-layer architecture was chosen.
In more detail the logic was seperated into a view-, a businesslogic- aswell as a database-/dataaccess-layer.

- View-Layer: Is the accesspoint to the backend and can be found in the /apis folder.
- Businesslogic-Layer: The implementation of this layer can be found in the /bl folder.
- Database-/Dataaccess-Layer: Can be found in the /db folder.

Short description of other folders:
- backups: This folder is used for saves of the MongoDB database. To do so, the script in the services/backup.py can be used.
- configs: Here each user can define a own mashine-/local-config. More details can be found in the readme.md in this folder.
- model: In this folder the used models for the Object Document Mapper are defined.
- routes: Here are the mapping of the routes are defined.
- services: In this folder service functions like the decorators are defined. Furthermore functions that won't fit any other layer are defined here as well.                                  |

## Installation

If you want to work without the frontend you can do so and use this postman collection: https://www.getpostman.com/collections/a46c0b06c91af361fed4 

### Without Docker

To run the backend python 3.9 is required. 

- python3 -m pip install -r requirements.txt
- python3 server.py

### With Docker

- (sudo) docker-compose up
