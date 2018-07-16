#!/usr/bin/env python
# %% import external dependencies
from glob import glob
from os import remove
from os.path import dirname, join, basename, splitext, exists, relpath, getmtime
from typing import List, Set, Mapping
from time import sleep
from datetime import datetime, timedelta
from threading import Thread, active_count
from itertools import groupby

from preanalyze import call_preanalyzer


# %% parameters
maxworkers = 4
startinterval = 30


def workingdir(key: str) -> str:
    return f'C:\\Users\\uedalab\\Desktop\\preanalysis_daehyun\\test\\hit_files\\{key}'


def keypatt(lmafilename: str) -> str:
    key, _ = basename(lmafilename).rsplit('__', maxsplit=1)
    return key


def currentkeys() -> Mapping[str, float]:
    patt = 'C:\\Users\\uedalab\\Desktop\\preanalysis_daehyun\\test\\lma_files\\*.lma'
    globbed = glob(patt)
    return  {k: max(getmtime(f) for f in groupped)
             for k, groupped in groupby(globbed, keypatt) if not exists(workingdir(k))}


def targetlist(key: str) -> List[str]:
    patt = f'C:\\Users\\uedalab\\Desktop\\preanalysis_daehyun\\test\\lma_files\\{key}__*.lma'
    globbed = glob(patt)
    return sorted(globbed)


# %%
def todolist() -> Set[str]:
    print(f"[{datetime.now()}] Scanning lma files...")
    lastkeys = currentkeys()
    lastchecked = datetime.now()
    while True:
        if datetime.now() < lastchecked + timedelta(seconds=startinterval):
            sleep(startinterval)
            continue
        print(f"[{datetime.now()}] Scanning new lma files...")
        curr = currentkeys()
        lastchecked = datetime.now()
        yield sorted(k for k in curr if k in lastkeys and curr[k] <= lastkeys[k])
        lastkeys = curr


def islocked(key: str) -> bool:
    wdir = workingdir(key)
    locker = f'{wdir}.locked'
    return exists(locker)


def work(key: str) -> None:
    wdir = workingdir(key)
    locker = f'{wdir}.locked'
    print(f"[{datetime.now()}] Working on key '{key}'...")
    with open(locker, 'w'):
        call_preanalyzer(lmafilelist=targetlist(key), workingdir=wdir)
    remove(locker)


# %% inf loop
for jobs in todolist():
    for key in jobs:
        if not islocked(key) and active_count()-1 < maxworkers:
            job = Thread(target=work, args=[key])
            job.start()
