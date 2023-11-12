from apscheduler.events import JobEvent

from utils.dbconnect import delete_task


def delete_task_from_db(job: JobEvent) -> None:
    delete_task(job.job_id)
