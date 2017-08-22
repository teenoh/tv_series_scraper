import json

from logging import getLogger

from .models import (Series, Seasons, Episodes)
from .scraper import scrape_data
from background_task import background

logger = getLogger(__name__)


@background(schedule=60)
def update_db():
    series_data = scrape_data()
    for series, series_details in series_data.items():
        if Series.objects.filter(name=series):
            ser = Series.objects.get(name=series)
        else :
            ser = Series.objects.create(name=series)
            ser.save()
            print("\nit got here sha " + ser.name)
            print("updated {ser}'s name".format(ser=ser.name))

        for season, season_details in series_details.items():
            if Seasons.objects.filter(name=season, series=ser):
                sea = Seasons.objects.get(name=season, series=ser) 
            else:
                sea = Seasons.objects.create(name=season, series=ser)
                sea.save()
                print("updated {ser}-{sea} name".format(ser=ser.name, sea=sea.name))

            for episode, episode_details in season_details.items():
                if Episodes.objects.all().filter(name=episode,
                                               download_link=episode_details,
                                               season=sea):
                    epis = Episodes.objects.get(name=episode,
                                                   download_link=episode_details,
                                                   season=sea)
                
                else :
                    epis = Episodes.objects.create(name=episode,
                                                   download_link=episode_details,
                                                   season=sea)
                    epis.save()
                    print("updated {ser}-{sea}-{epis} name".format(ser=ser.name,
                                                               sea=sea.name,
                                                               epis=epis.name))
    print("completed baby")


update_db(repeat=7200, repeat_until=None)
