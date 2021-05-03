#coding: utf-8
from models.metaData import MetaData
import uuid
import json

class MetaDataDatabase():

    def get(self, uid):
        # pylint: disable=no-member
        return MetaData.objects(uid__exact = uid).get()

    def getList(self, page, limit, fieldToOrder, asc, search):
        # pylint: disable=no-member
        if search == None:
            return MetaData.objects.order_by(fieldToOrder).paginate(page=page, per_page=limit)
        else:
            return MetaData.objects.search_text(search).order_by(fieldToOrder).paginate(page=page, per_page=limit) 
    
    def put(self, uid, comment, annotatedSchema, humanReadableName):
        # pylint: disable=no-member
        mD = MetaData.objects(uid__exact = uid).get()
        mD.comment = comment
        mD.schema=annotatedSchema.replace("\'", "\"").replace(" ", "").replace("True","true").replace("False","false")
        mD.humanReadableName=humanReadableName
        mD.save()
        return mD
    
    def delete(self, uid):
        try:
            # pylint: disable=no-member
            MetaData.objects(uid__exact=uid).delete()
        except:
            return False
        return True
