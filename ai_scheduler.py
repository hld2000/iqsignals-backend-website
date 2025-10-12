from apscheduler.schedulers.background import BackgroundScheduler
from ai_signal import generate_and_publish
scheduler = BackgroundScheduler()
JOB_ID = 'ai_signal_job'
def start_scheduler(interval_seconds=300, **kwargs):
    if scheduler.get_job(JOB_ID):
        return
    scheduler.add_job(lambda: generate_and_publish(**kwargs), 'interval', seconds=interval_seconds, id=JOB_ID, max_instances=1)
    scheduler.start()
def stop_scheduler():
    if scheduler.get_job(JOB_ID):
        scheduler.remove_job(JOB_ID)
