# Celery tasks
import logging
import itertools
from celery.task import task

from lizard_area.models import Area
from lizard_layers.models import AreaValue
from lizard_layers.models import ValueType
from lizard_layers.models import ParameterType
from lizard_fewsnorm.models import TimeSeriesCache
from lizard_measure.models import Score
from lizard_task.handler import get_handler
from lizard_task.task import task_logging


logger = logging.getLogger(__name__)


def update_area_value(area, value, value_type,
                      flag=None, comment=None, timestamp=None):
    area_value, created = AreaValue.objects.get_or_create(
        area=area,
        value_type=value_type,
    )
    area_value.object_information = unicode(area)
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

    See also GS060
    """
    if None in judgements:
        # 'doelbereik onbekend' (wordt niet getoond): van minimaal 1
        # EKR-indicator ontbreekt de score en/of de doelstelling voor
        # 2015
        return None
    if (min(judgements) == 1 and
        len([j for j in judgements if j > 1]) >= 2):
        # 'doel ruimschoots bereikt' (bijv: VV): de scores van alle 4
        # EKR-indicatoren voldoen aan de doelstelling van 2015 en
        # minimaal 2 EKR-indicatoren hebben al een hogere score
        return 2
    if (min(judgements) == 1 and
        len([j for j in judgements if j > 1]) < 2):
        # 'doel bereikt' (bijv: V): de scores van alle 4
        # EKR-indicatoren voldoen aan de doelstelling van 2015, maar
        # er zijn geen 2 EKR-indicatoren die een hogere score hebben
        return 1
    if len([j for j in judgements if j < 1]) == 1:
        # 'doel nog niet bereikt' (bijv: -): de score van 1
        # EKR-indicator voldoen nog niet aan de doelstelling van 2015,
        # de andere 3 al wel
        return -1
    if len([j for j in judgements if j < 1]) > 1:
        # 'doel nog lang niet bereikt' (bijv: --): de score van
        # minimaal 2 EKR-indicatoren voldoen nog niet aan de
        # doelstelling van 2015
        return -2


@task
def sync_ekr(username=None, taskname=None, dataset=None, loglevel=20):
    # Set up logging
    handler = get_handler(username=username, taskname=taskname)
    logger.addHandler(handler)
    logger.setLevel(loglevel)

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
            # value_worst = min([v['value'] for v in values
            #                    if v['value'] is not None])
            value_worst = min(values, key=lambda v: v['value'])
        except ValueError:
            # All ekrs are None
            value_worst = None

        if value_worst is not None:
            update_area_value(
                area=area,
                value=value_worst['value'],
                comment=value_worst['comment'],
                value_type=value_type_worst,
                )
        else:
            update_area_value(
                area=area,
                value=None,
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
        logger.debug('worst: %s, overall: %s' % (
                str(value_worst), overall_judgement))

    logger.info('Finished')

    # Remove logging handler
    logger.removeHandler(handler)

    return 'OK'


@task
@task_logging
def sync_ekr_goals(username=None, taskname=None, loglevel=20):
    """
    Make AreaValues for value types EKR-VIS-GOAL-2015,
    EKR-VIS-GOAL-2027, etc.

    Run this once in a while.
    """

    def update_value_types(measuring_rod_code):
        value_type_name = 'EKR-%s' % measuring_rod_code
        value_type, created = ValueType.objects.get_or_create(
            name=value_type_name)
        value_types[value_type_name] = value_type

        value_type_2015_name = 'EKR-%s-GOAL-2015' % measuring_rod_code
        value_type_2015, created_2015 = ValueType.objects.get_or_create(
            name=value_type_2015_name)
        value_types[value_type_2015_name] = value_type_2015

        value_type_2027_name = 'EKR-%s-GOAL-2027' % measuring_rod_code
        value_type_2027, created_2027 = ValueType.objects.get_or_create(
            name=value_type_2027_name)
        value_types[value_type_2027_name] = value_type_2027

        return (value_type if created else None,
                value_type_2015 if created_2015 else None,
                value_type_2027 if created_2027 else None)

    def update_area_value(score):
        """
        Make AreaValue from score.
        A score is associated with an (krw) area.
        """
        logger.debug('Updating for score: %s' % score)
        measuring_rod_code = score.measuring_rod.code

        value_type_2015 = value_types['EKR-%s-GOAL-2015' % measuring_rod_code]
        area_value_2015, created_2015 = AreaValue.objects.get_or_create(
            area=score.area, value_type=value_type_2015,
            defaults={'comment': score.target_2015})
        if not created_2015:
            area_value_2015.comment = score.target_2015
            area_value_2015.save()

        value_type_2027 = value_types['EKR-%s-GOAL-2027' % measuring_rod_code]
        area_value_2027, created_2027 = AreaValue.objects.get_or_create(
            area=score.area, value_type=value_type_2027,
            defaults={'comment': score.target_2027})
        if not created_2027:
            area_value_2027.comment = score.target_2027
            area_value_2027.save()

        return (area_value_2015 if created_2015 else None,
                area_value_2027 if created_2027 else None)

    logger = logging.getLogger(taskname)

    logger.info('Updating AreaValue EKR goalscores')

    measuring_rod_codes = ['VIS', 'FYTOPL', 'MAFAUNA', 'OVWFLORA']
    scores = Score.objects.filter(
        measuring_rod__code__in=measuring_rod_codes)

    value_types = {}
    result = map(update_value_types, measuring_rod_codes)
    result_created = filter(None, list(itertools.chain(*result)))
    if result_created:
        logger.info(
            'Created ValueType(s): %r' % result_created)

    logger.info('Updating area values for %d scores...' % len(scores))
    result = map(update_area_value, scores)
    result_list = list(itertools.chain(*result))
    logger.info('Updated %d AreaValues.' % len(result_list))
    result_created = filter(None, result_list)
    if result_created:
        logger.info('Created AreaValues:')
        for area_value in result_created:
            logger.info(' %s' % area_value)

    logger.info('Finished.')


@task
def sync_esf(username=None, taskname=None):
    # Set up logging
    handler = get_handler(username=username, taskname=taskname)
    #logger = logging.getLogger(taskname or __name__)
    logger.addHandler(handler)
    logger.setLevel(20)

    # Actual code to do the task
    logger.info('sync_esf')
    logger.info('DELETE ME')

    # Remove logging handler
    logger.removeHandler(handler)

    return 'TODO'
