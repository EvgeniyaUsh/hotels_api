from src.tasks.celery_app import celery_inst


@celery_inst.task
def main_task():
    print("Hello from the main task!")
