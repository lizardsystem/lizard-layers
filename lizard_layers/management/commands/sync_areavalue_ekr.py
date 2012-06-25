#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

# This sync function has dependencies on lizard_measure. So include
# lizard_measure in your INSTALLED_APPS.

from django.db import transaction
from django.core.management.base import BaseCommand

from lizard_layers.tasks import sync_ekr
from lizard_layers.tasks import sync_ekr_goals

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Synchronizes ESF and EKR in datasources into cache table.
    """

    @transaction.commit_on_success
    def handle(self, *args, **options):
        sync_ekr(taskname=options.get('taskname', None), loglevel=10)
        sync_ekr_goals(taskname=options.get('taskname', None), loglevel=10)
