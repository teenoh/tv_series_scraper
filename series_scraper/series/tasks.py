import json

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .models import (Series, Seasons, Episodes)
logger = get_task_logger(__name__)

@periodic_task(run_every=(crontab(minute='*/2')), name="some_task", ignore_result=True)
def some_task():
    update_db()
    logger.info("Updated db")


def update_db():
    with open('../data.json', 'r') as fp:
        data = json.load(fp)
        fp.close()
    for series, series_details in data.items():
        ser = Series.objects.get(name=series)
        if not ser:
            ser = Series.objects.create(name=series)
            ser.save()
            print("updated {ser}'s name".format(ser=ser.name))

        for season, season_details in series_details.items():
            sea = Seasons.objects.get(name=season, series=ser)
            if not sea:
                sea = Seasons.objects.create(name=season, series=ser)
                sea.save()
                print("updated {ser}-{sea} name".format(ser=ser.name, sea=sea.name))

            for episode, episode_details in season_details.items():
                epis = Episodes.objects.get(name=episode,
                                               download_link=episode_details,
                                               season=sea)
                if not epis:
                    epis = Episodes.objects.create(name=episode,
                                                   download_link=episode_details,
                                                   season=sea)
                    epis.save()
                    print("updated {ser}-{sea}-{epis} name".format(ser=ser.name,
                                                               sea=sea.name,
                                                               epis=epis.name))
    print("completed baby")