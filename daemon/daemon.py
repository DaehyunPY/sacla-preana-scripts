"""
Preanalyzing daemon.
"""
# %% import external dependencies
from glob import glob
from os import remove
from os.path import basename, exists, getmtime, splitext
from typing import List, Set, Mapping
from time import sleep
from datetime import datetime
from threading import Thread, active_count
from itertools import groupby

from .aprocess import call_aprocess


__all__ = ['run']


# %% parameters
maxworkers = 3*3
startinterval = 30


def workingdir(key: str) -> str:
    """
    Working dir where a preanalyzing process works.
    """
    return f'D:\\2018B8014Kukk\\hit_files\\{key}'


def keypatt(lmafilename: str) -> str:
    """
    A rule (pattern) getting keys from lma filenames, where key is unique str indentifying lma file groups.
    In other words, files having the same key belong to the same group. For example, if we define the function as...

    keypatt(lmafilename: str) -> str:
        from os.path import basename
        key, _ = basename(lmafilename).rsplit('__', maxsplit=1)
        return key
    
    then, these two files 'aq001__0000.lma' and 'aq001__0001.lma' have the same key 'aq001'; they will be preanalyzed
    as the same lma group.
    """
    # key, _ = basename(lmafilename).rsplit('__', maxsplit=1)
    key, _ = splitext(basename(lmafilename))
    return key


def targetlist() -> List[str]:
    """
    Target lma file list.
    """
    return glob('Z:\\2018B8014Kukk\\lma_files\\aq*.lma')


def currentkeys() -> Mapping[str, float]:
    """
    Current keys (lma file groups) have to be preanalyzed and their last modifed timestamp.
    Do not return keys which already have been analyzed.
    """
    mtimes = {k: max(getmtime(f) for f in groupped)
              for k, groupped in groupby(targetlist(), keypatt)}
    return {k: m for k, m in mtimes.items()
            if not exists(workingdir(k)) or getmtime(workingdir(k)) < m}


# %%
def todolist() -> Set[str]:
    print(f"[{datetime.now()}] Scanning lma files...")
    lastkeys = currentkeys()
    sleep(startinterval)
    while True:
        print(f"[{datetime.now()}] Scanning new lma files...")
        curr = currentkeys()
        # do not read very last run and flip the order
        yield sorted(k for k in curr if k in lastkeys and curr[k] <= lastkeys[k])
        lastkeys = curr
        sleep(startinterval)


def islocked(key: str) -> bool:
    wdir = workingdir(key)
    locker = f'{wdir}.locked'
    return exists(locker)


def work(key: str) -> None:
    wdir = workingdir(key)
    locker = f'{wdir}.locked'
    print(f"[{datetime.now()}] Working on key '{key}'...")
    with open(locker, 'w'):
        call_aprocess(lmafilelist=[f for f in targetlist() if keypatt(f) == key],
                      workingdir=wdir)
    remove(locker)


# %% inf loop
def run() -> None:
    for jobs in todolist():
        print(f"[{datetime.now()}] Todo list: {' '.join(jobs)}")
        for key in jobs:
            if not islocked(key) and active_count()-1 < maxworkers:
                job = Thread(target=work, args=[key])
                job.start()
