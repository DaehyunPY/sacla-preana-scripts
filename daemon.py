#!/usr/bin/env python3
# %% import external dependencies
from glob import glob
from os import remove
from os.path import dirname, join, basename, splitext, exists
from typing import List, Set
from time import sleep
from datetime import datetime
from threading import Thread, active_count


# %% parameters
maxworkers = 3


def targetlist() -> Set[str]:
    patt = 'C:\\Users\\uedalab\\Desktop\\preanalysis_daehyun\\test\\lma_files\\*.lma'
    return set(glob(patt))


def outputpath(target: str) -> str:
    par = dirname(target)
    key, _ = splitext(basename(target))
    return join(par, '..', 'hit_files', key)


# %%
def todolist() -> Set[str]:
    targets = targetlist()
    return {t for t in targets if not exists(outputpath(t))}


def islocked(target: str) -> bool:
    out = outputpath(target)
    locker = f'{out}.locked'
    return exists(locker)


def work(target: str) -> None:
    out = outputpath(target)
    locker = f'{out}.locked'
    print(f"[{datetime.now()}] Working on target '{target}'...")
    with open(locker, 'w'):
        with open(out, 'w'):
            sleep(10)
    remove(locker)


# %% inf loop
while True:
    for target in todolist():
        if not islocked(target) and active_count()-1 < maxworkers:
            job = Thread(target=work, args=[target])
            job.start()
    sleep(30)
