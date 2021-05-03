#coding: utf-8
from db.metaData import MetaDataDatabase
from models.metaData import MetaData
import json

def mapper(metaData: MetaData):

    return{
        "uid":metaData.uid,
        "sourceConnection":metaData.sourceConnection,
        "sourceUser":metaData.sourceUser,
        "sourcePassword":metaData.sourcePassword,
        "sourceDBName": metaData.sourceDBName,
        "sourceCollectionOrTableName": metaData.sourceCollectionOrTableName,
        "isDatabase": metaData.isDatabase,
        "schema": json.loads(metaData.schema),
        "insertedAt": metaData.insertedAt.isoformat(),
        "comment": metaData.comment if metaData.comment is not None else "",
        "targetStorageSystem": metaData.targetStorageSystem,
        "targetURL": metaData.targetURL,
        "mimetype": metaData.mimetype,
        "insertedBy": metaData.insertedBy.fetch().firstname + ' ' + metaData.insertedBy.fetch().lastname,
        "csvHasHeader": metaData.csvHasHeader if metaData.csvHasHeader is not None else "",
        "csvDelimiter": metaData.csvDelimiter if metaData.csvDelimiter is not None else "",
        "humanReadableName": metaData.humanReadableName if metaData.humanReadableName is not None else "",
        "xmlRowTag": metaData.xmlRowTag if metaData.xmlRowTag is not None else "",
        "heritage": metaData.heritage,
        "constructionCode": metaData.constructionCode if metaData.constructionCode is not None else "",
        "constructionQuery": metaData.constructionQuery if metaData.constructionQuery is not None else ""
    }
        

class MetaDataBusinessLogic():
    db = MetaDataDatabase()

    def get(self, uid):
        metaData = self.db.get(uid)
        return {'metaData':mapper(metaData)}
    
    def getList(self, page, limit, fieldToOrder, asc, search):
        if not asc:
                fieldToOrder = '-'+fieldToOrder
        metaDatas = self.db.getList(page, limit, fieldToOrder, asc, search)
        metaDataList = []  
        for mD in metaDatas.items:
            metaDataList.append(mapper(mD))
        return {'metaDatas':metaDataList, "total":metaDatas.total}
  
    def put(self, uid, comment, annotatedSchema, humanReadableName):
        metaData = self.db.put(uid, comment, annotatedSchema, humanReadableName)
        return {'metaData':mapper(metaData)}

    def delete(self, uid):
        return self.db.delete(uid)

    