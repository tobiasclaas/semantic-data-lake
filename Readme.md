# Semantic Data Lake

Welcome to the Semantic Data Lake Project. Our Program manages big datasets and allows for Ingestion, Storage, Annotation and Transformation
of Big Data.

## Installation and Configuration
We strongly recommend using Linux to run the System due to configuration issues with docker on other OS.

### Linux
* python version
  * The suggested Python version is 3.8.10 but later releases should also work.
* docker
  * You need to install Docker to run you application since we run all components in docker containers to ensure maximal portability.
* virtual environment
  * To run the program you need some modules with specific versions to ensure the correct behavior of the system.
  For that you may want to create a virtual environment such that there are no conflicts with other module versions.
  * When you are ready to install the requirements, navigate to ".../team-2-data-lake/code/backend/src" and run:\
    `pip freeze > requirements.txt` \
    `pip install -r requirements.txt` \
    `pip list --format=freeze > requirements.txt`

## Run the Program
### Linux
* First go through the installation and configuration guide
* Launch in production mode:
  * Login to our docker hub account to have access to the repo. Credentials: user:semanticdatalake21 and password:DataLake2021
  * Navigate to docker/full
  * and run `(sudo) docker-compose up`
  * this command will download a bunch of docker containers (15 in total, approx. 15 GB Disk space)
* Launch in development mode:
  * Navigate to docker/dev and run `(sudo) docker-compose up`, make sure to delete the ./data folder beforehand if present
  * Navigate to code/backend/src
  * and run `python3 server.py`
* Authentication
  * To be able to use the app you need to authenticate to the system. Either with credentials \
    Username: admin, Password: admin or \
    Username: user, Password: user.

## Structure of the Project
The project has three main folders: code, docker and documents.

### Code
Here you can find the Code for the project, splitted in frontend and backend. The src folder in backend is again divided
into relatively self explaining modules: api, utils, database and resource. API handles all requests coming from
the web page and processes them with the help of utils and database. Whenever a database is accessed a function
in directory workspace is called to provide a good degree of abstraction. The resource folder simply contains one file
with the default ontology we are providing by default.

### Docker
Here the docker container configurations are stored. full differs from dev only by our application container, that contains the projects code and launches the back- and frontend. 

### Documents
Here you can find presentation slides, organizational stuff and sample data for testing.

## Documentation

### PyDocs
* We documented the code with PyDoc comments which are visible in the code itself or can be viewed in HTML format.
* For the PyDocs in HTML format navigate to ".../team-2-data-lake/code/backend/src" and run: \
 `pydoc -p <port>`  and press `b` afterwards to open the documentation in the browser.

### Frontend
* Until now, no documentation.

### APIs
* RESTAPIs are used for the communication between frontend and backend. To enable easy testing and traceability we provide a
  postman JSON file with all methods, and their according routes which can can also find in the resouces folder 
  and in the [Wiki](https://git.rwth-aachen.de/lab-semantic-data-integration-2021/team-2-data-lake/-/wikis/home).

### Components
We provided a more detailed documentation see the [Github Wiki](https://git.rwth-aachen.de/lab-semantic-data-integration-2021/team-2-data-lake/-/wikis/home)

* Possible Problems during Setup:
  * Sometimes, especially when working on remote machines, on needs to set static ip adresses. The relevant lines are commented: https://git.rwth-aachen.de/lab-semantic-data-integration-2021/team-2-data-lake/-/blob/master/docker/dev/docker-compose.yml#L173
  * On some machines we faced issues with the network reachability of the hadoop cluster. Put the namenode and datanodes to the /etc/hosts file      pointing to localhost ip adress.
  * On repeated Startup some containers might fail (especially fuseki)
  * deletion of data folder in directory docker/dev and/or docker/full is necessary. Also remove the containers via docker rm -f fuseki.

###### BY Sayed Hoseini, Muhammad Noman, Tobias Claas, Maher Fallouh & Zaid Abdullah @2021
