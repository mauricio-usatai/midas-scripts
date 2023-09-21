import time

import schedule
from utils import DotSpinner

from dag import run_dag


schedule.every().day.at("20:50").do(run_dag)
spinner = DotSpinner("Waiting")

while True:
    schedule.run_pending()
    next(spinner)
    time.sleep(0.1)
