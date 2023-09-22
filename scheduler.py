import time
from textwrap import dedent
from datetime import datetime

import schedule

from utils import (
    DotSpinner,
    SMSMessenger,
)
from dag import dag
from settings import Settings


settings = Settings()


def run_dag():
    dag()

    messenger = SMSMessenger()
    messenger.send(dedent(
        f'''Midas workflow completed at {datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}'
        for news query: {settings.NEWS_KEYWORDS}'''
    ))


schedule.every().day.at("20:50").do(run_dag)
spinner = DotSpinner("Waiting")

while True:
    schedule.run_pending()
    next(spinner)
    time.sleep(0.1)
