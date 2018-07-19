"""
Preanalyze lma files and save (t,x,y) data in root/hit format.
"""
# %% import external dependencies
from typing import List, Iterable
from os import makedirs
from os.path import join, basename, realpath, relpath
from textwrap import dedent
from subprocess import call
from warnings import warn


__all__ = ['call_preanalyzer']


# %% parameters
templatepath = 'template.txt'
lma2rootpath = 'C:\\home\\programs\\lma2root_SACLA\\Binaries\\lma2root.exe'


# %%
with open(templatepath, 'r') as f:
    template = f.read()


def call_preanalyzer(lmafilelist: Iterable[str], workingdir: str) -> None:
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

    with open(join(f'{workingdir}', 'resort.bat'), 'w') as f:
        f.write(dedent(
            f"""\
            pushd {workingdir}
            {lma2rootpath} < resort.txt 1> resort.log 2> resort.err
            """
        ))
    call(join(f'{workingdir}', 'resort.bat'))
