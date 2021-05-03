#coding: utf-8
import uuid
from models.job import Job

class JobDatabase():

    def get(self, uid):
        # pylint: disable=no-member
        return Job.objects(uid__exact = uid).get()

    def getList(self, page, limit, fieldToOrder, asc, search):
        # pylint: disable=no-member
        if search == None:
            return Job.objects.order_by(fieldToOrder).paginate(page=page, per_page=limit)
        else:
            return Job.objects.search_text(search).order_by(fieldToOrder).paginate(page=page, per_page=limit) 

    def delete(self, uid):
        try:
            # pylint: disable=no-member
            Job.objects(uid__exact=uid).delete()
        except:
            return False
        return True