from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.triggers.base import BaseTrigger



class Scheduler:
    
    def __init__(self):
        jobstores = {
            'default': MemoryJobStore()
            }
        executors = {
            'default': AsyncIOExecutor()
            }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
            }
        self.scheduler = AsyncIOScheduler(
            jobstores=jobstores, 
            executors=executors, 
            job_defaults=job_defaults
            )
        
    def add_job(self, trigger: BaseTrigger, job):
        self.scheduler.add_job(
            func=job.process, 
            trigger=trigger,
            id="outbox_job",
            replace_existing=True
            )
    
    def start(self):
        self.scheduler.start()