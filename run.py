# $ pipenv run python ./run.py
from daemon import call_aprocess


lmafilelist = """
path\\to\\file0.lma
path\\to\\file1.lma
path\\to\\file2.lma
""".split()
workingdir = "path\\to\\dir"

call_aprocess(
    lmafilelist=lmafilelist,
    workingdir=workingdir,
)
