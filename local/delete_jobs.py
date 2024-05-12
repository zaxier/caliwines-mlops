from databricks.sdk import WorkspaceClient


def filter_job_list(search_string: str, limit: int = 1000):
    job_list = w.jobs.list(expand_tasks=False)
    i = 0
    while True:
        job = next(job_list)
        if search_string in job.settings.name:
            yield job

        i += 1

        if i > limit:
            break


w = WorkspaceClient(profile="azure-field-eng-east")
search_string = "poc-accelerate-mlops"
for job in filter_job_list(search_string):
    print("Deleting job: ", job.settings.name)
    w.jobs.delete(job_id=job.job_id)


w = WorkspaceClient(profile="DEFAULT")
search_string = "poc-accelerate-mlops"
for job in filter_job_list(search_string):
    print("Deleting job: ", job.settings.name)
    w.jobs.delete(job_id=job.job_id)
