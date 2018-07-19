"""
Preanalyze lma files and save (t,x,y) data in root/hit format.
"""
# %% import external dependencies
from typing import Iterable
from os import makedirs, environ
from os.path import join, basename, realpath, relpath
from subprocess import call
from warnings import warn

from importlib_resources import read_text

from . import rsc


__all__ = ['call_aprocess']


# %%
exe = environ['LMA2ROOT']
template = read_text(rsc, 'template.txt')


def call_aprocess(lmafilelist: Iterable[str], workingdir: str) -> None:
    workingdir = realpath(workingdir)
    lmafilelist = [relpath(f, workingdir) for f in lmafilelist]
    goodlist = [f for f in lmafilelist if ' ' not in f]
    if len(goodlist)!=len(lmafilelist):
        warn('One or more lma files skipped because their paths include space!')
    makedirs(workingdir, exist_ok=True)
    key = basename(workingdir)

    with open(join(f'{workingdir}', 'resort.txt'), 'w') as f:
        f.write(template.format(
            basename=f'{key}',
            lmafilelist='\n'.join(goodlist),
        ))
    call(exe, cwd=workingdir, stdin="resort.txt", stdout="log.out", stderr="log.err")
