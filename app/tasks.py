import time

import rq


def example(seconds):
    job = rq.get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['PROGRESS'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['PROGRESS'] = 100
    job.save_meta()
    print('Task completed')