#!/usr/bin/env python3
# %% import external dependencies
from os import makedirs
from os.path import join, basename, realpath
from textwrap import dedent
from subprocess import call


__all__ = ['call_preanalyzer']


# %% parameters
templatepath = 'C:\\Users\\uedalab\\Desktop\\preanalysis_daehyun\\template.txt'
lma2rootpath = 'C:\\home\\programs\\lma2root_SACLA\\Binaries\\lma2root.exe'


# %%
with open(templatepath, 'r') as f:
    template = f.read()


def call_preanalyzer(lmafilename: str, workingdir: str) -> None:
    lmafilename = realpath(lmafilename)
    workingdir = realpath(workingdir)
    makedirs(workingdir, exist_ok=True)
    key = basename(workingdir)

    with open(join(f'{workingdir}', 'resort.txt'), 'w') as f:
        f.write(template.format(
            basename=f'{key}',
            lma_filelist=lmafilename,
        ))

    with open(join(f'{workingdir}', 'resort.bat'), 'w') as f:
        f.write(dedent(
            f"""\
            pushd {workingdir}
            {lma2rootpath} < resort.txt > resort.log
            """
        ))
    call(join(f'{workingdir}', 'resort.bat'))
