#coding: utf-8
from db.job import JobDatabase
from models.job import Job

def mapper(job: Job):
    endedAt = None
    try: 
        endedAt = job.endedAt.isoformat()
    except:
        endedAt = None

    # delete job if it's invalid with faulty uid
    if not job.uid or job.uid == "":
        job.delete()
        return None

    user = job.startedBy.fetch()
    return{
        "uid":job.uid,
        "task": job.task,
        "startedBy":user.firstname + ' ' + user.lastname,
        "errorMessage": job.errorMessage,
        "startedAt": job.startedAt.isoformat(),
        "failed": job.failed,
        "endedAt": endedAt
    }


        

class JobBusinessLogic():
    db = JobDatabase()

    def get(self, uid):
        job = self.db.get(uid)
        return {'job':mapper(job)}
    
    def getList(self, page, limit, fieldToOrder, asc, search):
        if not asc:
            fieldToOrder = '-'+fieldToOrder
        jobs = self.db.getList(page, limit, fieldToOrder, asc, search)
        jobList = []  
        for j in jobs.items:
            mapped = mapper(j)
            jobList.append(mapped)
        return {'jobs':jobList, 'total':jobs.total}

    def delete(self, uid):
        return self.db.delete(uid)
  


    
