# Semantic Data Lake

## Welcome

## Installation and Configuration
* python version
  * The suggested Python version is 3.8.10 but later releases should also work.
* docker
  * You need to install Docker to run you application since we run all components in docker containers to ensure maximal portability.
  * TODO describe how to start application if it is in only one container
* virtual environment
  * To run the program you need some modules with specific versions to ensure the correct behavior of the system.
  For that you may want to create a virtual environment such that there are no conflicts with other module versions.
  * When you are ready to install the requirements, navigate to ".../team-2-data-lake/code/backend/src" and run:
    `pip freeze > requirements.txt` \
    `pip install -r requirements.txt` \
    `pip list --format=freeze > requirements.txt`

* Possible Problems during Setup:
  * TODO add more
  * The Thing where you need to add the table for the ?port forwarding?
  * On repeated Startup some containers might fail (especially fuseki)
    * deletion of data folder and docker container is necessary then

## Structure of the Project
The project has three main folders: code, docker and documents.

### Code
Here you can find the Code for the project, splitted in frontend and backend. The src folder in backend is again divided
into relatively self explaining modules: api, business_logic, database and resource. API handles all requests coming from
the web page and processes them with the help of business_logic and database. Whenever a database is accessed a function
in directory workspace is called to provide a good degree of abstraction. The resource folder simply contains one file
with the default ontology we are providing by default.

### Docker
Here the docker container configurations are stored.

### Documents
Here you can find presentation slides, organizational stuff and sample data for testing.

## Documentation

### PyDocs
* We documented the code with PyDoc comments which are visible in the code itself or can be viewed in HTML format.
* For the PyDocs in HTML format navigate to ".../team-2-data-lake/code/backend/src" and run: \
 `pydoc -p <port>` \
 and press `b` afterwards

### Frontend
* Until now, no documentation

### APIs
* We decided to use RESTAPIs as APIs between frontend and backend. To enable easy testing and traceability we provide a
postman JSON file with all method and their according routes which can can also find in the [Wiki](https://git.rwth-aachen.de/lab-semantic-data-integration-2021/team-2-data-lake/-/wikis/home)

### Components
We provided a more detailed documentation see the [Github Wiki](https://git.rwth-aachen.de/lab-semantic-data-integration-2021/team-2-data-lake/-/wikis/home)



###### BY Sayed Hoseini, Muhammad Noman, Tobias Claas, Maher Fallouh & Zaid Abdullah @2021