from apscheduler.events import JobEvent

from db.orm import SyncORM


def delete_task_from_db(job: JobEvent) -> None:
    SyncORM.delete_task(job.job_id)
