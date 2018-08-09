#! /usr/bin/env python
# map-ephys interative shell

import os
import sys
import logging
import warnings
from code import interact

import datajoint as dj

from pipeline import ephys
from pipeline import lab
from pipeline import experiment
from pipeline import ccf
from scripts import ingestBehavior
from scripts import ingestEphys

log = logging.getLogger(__name__)
__all__ = [ephys, lab, experiment, ccf, ingestBehavior, ingestEphys]
[ dj ]  # NOQA flake8 

warnings.simplefilter(action='ignore', category=FutureWarning)


def usage_exit():
    print("usage: {p} [populateB|populateE|shell|erd]"
          .format(p=os.path.basename(sys.argv[0])))
    sys.exit(0)


def logsetup(*args):
    logging.basicConfig(level=logging.ERROR)
    log.setLevel(logging.DEBUG)
    logging.getLogger('ingest').setLevel(logging.DEBUG)
    logging.getLogger('scripts.ingestBehavior').setLevel(logging.DEBUG)
    logging.getLogger('scripts.ingestEphys').setLevel(logging.DEBUG)


def populateB(*args):
    ingestBehavior.BehaviorIngest().populate(display_progress=True)


def populateE(*args):
    ingestEphys.EphysIngest().populate(display_progress=True)


def shell(*args):
    interact('map shell.\n\nschema modules:\n\n  - {m}\n'
             .format(m='\n  - '.join(str(m.__name__) for m in __all__)),
             local=globals())


def erd(*args):
    for mod in (ephys, lab, experiment, ccf,):
        modname = str().join(mod.__name__.split('.')[1:])
        fname = '{}.png'.format(modname)
        print('saving', fname)
        dj.ERD(mod, context={modname: mod}).save(fname)


actions = {
    'populateB': populateB,
    'populateE': populateE,
    'shell': shell,
    'erd': erd,
}

if __name__ == '__main__':

    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        usage_exit()

    logsetup()

    action = sys.argv[1]
    actions[action](sys.argv[2:])
