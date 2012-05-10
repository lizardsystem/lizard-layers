# Celery tasks
import logging
from celery.task import task

from lizard_area.models import Area
from lizard_layers.models import AreaValue
from lizard_layers.models import ValueType
from lizard_layers.models import ParameterType
from lizard_fewsnorm.models import TimeSeriesCache
from lizard_measure.models import Score
from lizard_task.handler import get_handler


logger = logging.getLogger(__name__)


def update_area_value(area, value, value_type,
                      flag=None, comment=None, timestamp=None):
    area_value, created = AreaValue.objects.get_or_create(
        area=area,
        value_type=value_type,
    )
    area_value.value = value
    area_value.flag = flag
    area_value.comment = comment
    area_value.timestamp = timestamp
    area_value.save()
    logger.debug('Updated area value: %s %s' % (area_value, value_type))
    return created


def _judgements(values, area):
    """
    Calculate individual judgements.
    """
    judgements = []
    for value in values:
        # TODO Performance improvement possible here.
        try:
            measuring_rod_code = value[
                'parameter_type'].measuring_rod_code
            score = Score.objects.get(
                measuring_rod__code=measuring_rod_code,
                area=area,
                )
            judgements.append(
                score.judgement(
                    value['comment'],
                    score.target_2015,
                    )
                )
        except Score.DoesNotExist:
            judgements.append(None)
    return judgements


def _overall_judgement(judgements):
    """
    Return overall judgement.
    """
    if None in judgements:
        return None
    if (min(judgements) == 1 and
        len([j for j in judgements if j > 1]) >= 2):
        return 2
    if (min(judgements) == 1 and
        len([j for j in judgements if j > 1]) < 2):
        return 1
    if len([j for j in judgements if j < 1]) == 1:
        return -1
    if len([j for j in judgements if j < 1]) > 1:
        return -2


@task
def sync_ekr(username=None, taskname=None, dataset=None):
    # Set up logging
    handler = get_handler(username=username, taskname=taskname)
    #logger = logging.getLogger(__name__)
    #logger = logging.getLogger(taskname or __name__)
    logger.addHandler(handler)
    logger.setLevel(20)

    logger.info('sync_ekr')

    # Actual code to do the task
    value_type_worst = ValueType.objects.get(name='EKR-ONGUNSTIG')
    value_type_score = ValueType.objects.get(name='EKR-DOELSCORE')

    parameter_types = list(ParameterType.objects.all())

    areas = Area.objects.filter(
        area_class=Area.AREA_CLASS_KRW_WATERLICHAAM,
        )
    if dataset:
        areas = areas.filter(data_set__name=dataset)
        logger.info('Data set: %s' % dataset)
    logger.info('Updating %d areas...' % areas.count())
    for area in areas:
        logger.debug('Updating area %s...' % area)
        values = []
        for parameter_type in parameter_types:
            timeseries = TimeSeriesCache.objects.filter(
                parametercache=parameter_type.parameter,
                geolocationcache__ident=area.ident,
            )
            value = None
            flag = None
            comment = None
            timestamp = None
            if timeseries:
                timeserie = timeseries[0]
                try:
                    event = timeserie.get_latest_event()
                    value = event.value
                    flag = event.flag
                    comment = event.comment
                    timestamp = event.timestamp
                except IndexError:
                    # No events at all
                    pass

            update_area_value(
                area=area,
                value=value,
                flag=flag,
                comment=comment,
                timestamp=timestamp,
                value_type=parameter_type.value_type,
            )
            values.append({
                'parameter_type': parameter_type,
                'value': value,
                'flag': flag,
                'comment': comment,
                'timestamp': timestamp,
            })

        try:
            value_worst = min([v['value'] for v in values
                               if v['value'] is not None])
        except ValueError:
            # All ekrs are None
            value_worst = None

        update_area_value(
            area=area,
            value=value_worst,
            comment=None,
            value_type=value_type_worst,
        )
        judgements = _judgements(values, area)
        overall_judgement = _overall_judgement(judgements)
        update_area_value(
            area=area,
            value=overall_judgement,
            comment=None,
            value_type=value_type_score,
        )

    logger.info('Finished')
    logger.removeHandler(handler)
    return 'OK'


@task
def sync_esf(username=None, taskname=None):
    # Set up logging
    handler = get_handler(username=username, taskname=taskname)
    #logger = logging.getLogger(taskname or __name__)
    logger.addHandler(handler)
    logger.setLevel(20)

    # Actual code to do the task
    logger.info('sync_esf')
    logger.info('TODO')

    logger.removeHandler(handler)
    return 'TODO'
