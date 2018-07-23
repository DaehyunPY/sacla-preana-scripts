"""
Preanalyze lma files and save (t,x,y) data in root/hit format.
"""
# %% import external dependencies
from textwrap import dedent
from typing import Iterable
from os import makedirs, environ
from os.path import join, basename, realpath
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
    goodlist = [f for f in lmafilelist if ' ' not in f]
    if len(goodlist)!=len(lmafilelist):
        warn('One or more lma files skipped because their paths include space!')
    makedirs(workingdir, exist_ok=True)
    key = basename(workingdir)
    inp = join(f'{workingdir}', 'resort.txt')
    job = join(f'{workingdir}', 'resort.bat')

    with open(inp, 'w') as f:
        f.write(template.format(
            basename=f'{key}',
            lmafilelist='\n'.join(goodlist),
        ))
    with open(job, 'w') as f:
        f.write(dedent(
            f"""\
            "{exe}" < resort.txt 1> resort.log 2> resort.err
            """
        ))
    call(job, cwd=workingdir)
