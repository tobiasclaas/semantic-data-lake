from db.user import UserDatabase
from flask import Flask
import psycopg2
from dbInit import FlaskDocument
from models.user import User


def register(app):
  PostgresSetup().run(app)
  # ResetDB().run()
  PopulateDB().run()


class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


class PostgresSetup:

  def run(self, app: Flask):
    connection = None
    host = app.config['POSTGRES_HOST']
    user = app.config['POSTGRES_USER']
    password = app.config['POSTGRES_PASSWORD']
    port = app.config['POSTGRES_PORT']
    database = app.config['POSTGRES_STORAGE_DB']

    try:
      connection = psycopg2.connect(
        f"host='{host}' user='{user}' password='{password}' port='{port}'"
      )
    except psycopg2.OperationalError as err:
      print(f"{bcolors.FAIL}[POSTGRES] error while creating:{bcolors.ENDC}\n\t{err}")

    if connection is not None:
      connection.autocommit = True
      cur = connection.cursor()
      cur.execute("SELECT datname FROM pg_database;")
      list_database = cur.fetchall()
      if  (database,) not in list_database:
        cur.execute(f"CREATE DATABASE {database};")
        print(f"{bcolors.OKGREEN}[POSTGRES] created storage database{bcolors.ENDC}")
      connection.close()


class ResetDB:

  def run(self):
    self.dropCollections()

  def dropCollections(self):
    for klass in FlaskDocument.all_subclasses():
      klass.drop_collection()


class PopulateDB:

  def run(self):
    try:
      # ResetDB().dropCollections()
      if len(User.objects().all()) == 0:
        self.createUsers()
        print(f"{bcolors.OKGREEN}[MONGODB] created administration{bcolors.ENDC}")
    except Exception as err:
      print(f"{bcolors.FAIL}[MONGODB] create administration failed{bcolors.ENDC}\n\t{err}")

  @staticmethod
  def createUsers():
    users = []
    for u in (
        ("mapro2020", "mapro2020", True, "Master", "Project"),
    ):
      user = User(
        email=u[0],
        password=User().generateHash(u[1]),
        isAdmin=u[2],
        firstname=u[3],
        lastname=u[4],
      )
      users.append(user)
    # pylint: disable=no-member
    User.objects.insert(users)
