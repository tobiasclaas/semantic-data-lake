#coding: utf-8
import uuid
from models.user import User

class UserDatabase():

    def get(self, email):
        # pylint: disable=no-member
        return User.objects(email__exact = email).get()

    def getList(self):
        # pylint: disable=no-member
        return User.objects.all()

    def put(self, email, isAdmin, firstname, lastname, password=None):
        # pylint: disable=no-member
        user = User.objects(email__exact = email).get()
        if password:
            user.password = User.generateHash(password)
        user.isAdmin = isAdmin
        user.firstname = firstname
        user.lastname = lastname
        user.save()
        return user
    
    def post(self, email, password, isAdmin, firstname, lastname):
        user = User(
            email=email,
            password=User().generateHash(password),
            isAdmin=isAdmin,
            firstname=firstname,
            lastname=lastname,
        )
        # pylint: disable=no-member
        User.objects.insert(user)
        return user
    
    def delete(self, email):
        try:
            # pylint: disable=no-member
            User.objects(email__exact=email).delete()
        except:
            return False
        return True
