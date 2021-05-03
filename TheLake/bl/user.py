#coding: utf-8
from db.user import UserDatabase
from models.user import User

def mapper(user):
    return{
        "email":user.email,
        "isAdmin":user.isAdmin,
        "firstname":user.firstname,
        "lastname":user.lastname,
    }
        

class UserBusinessLogic():
    db = UserDatabase()

    def get(self, email):
        user = self.db.get(email)
        return {'user':mapper(user)}
    
    def getList(self):
        users = self.db.getList()
        userList = []  
        for u in users:
            userList.append(mapper(u))
        return {'users':userList}
    
    def delete(self, email):
        return self.db.delete(email)

    def put(self, email, isAdmin, firstname, lastname, password):
        return {'user':mapper(self.db.put(email, isAdmin, firstname, lastname, password))}
    
    def post(self, email, password, isAdmin, firstname, lastname):
        return {'user':mapper(self.db.post(email, password, isAdmin, firstname, lastname))}
    
  


    